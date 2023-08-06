#! python3
# FanGraphs/leaders.py

"""
Web scraper for the FanGraphs **Leaders** webpages.
Each page which is covered has its own class for scraping it.
"""

import csv
import datetime
import os

from fangraphs import utilities
import fangraphs.exceptions
from fangraphs.selectors import leaders_sel


class MajorLeague(utilities.ScrapingUtilities):
    """
    Scrapes the FanGraphs `Major League Leaderboards`_ page.

    Note that the Splits Leaderboard is not covered.
    Instead, it is covered by :py:class:`SplitsLeaderboards`.

    .. _Major League Leaderboards: https://fangraphs.com/leaders.aspx
    """
    __selections = leaders_sel.MajorLeague.selections
    __dropdowns = leaders_sel.MajorLeague.dropdowns
    __dropdown_options = leaders_sel.MajorLeague.dropdown_options
    __checkboxes = leaders_sel.MajorLeague.checkboxes
    __buttons = leaders_sel.MajorLeague.buttons

    address = "https://fangraphs.com/leaders.aspx"

    def __init__(self, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset()

    @classmethod
    def list_queries(cls):
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :rtype: list
        """
        queries = []
        queries.extend(list(cls.__selections))
        queries.extend(list(cls.__dropdowns))
        queries.extend(list(cls.__checkboxes))
        return queries

    def list_options(self, query: str):
        """
        Lists the possible options which a filter query can be configured to.

        :param query: The filter query
        :return: Options which the filter query can be configured to
        :rtype: list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__checkboxes:
            options = ["True", "False"]
        elif query in self.__dropdown_options:
            elems = self.soup.select(f"{self.__dropdown_options[query]} li")
            options = [e.getText() for e in elems]
        elif query in self.__selections:
            elems = self.soup.select(f"{self.__selections[query]} li")
            options = [e.getText() for e in elems]
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return options

    def current_option(self, query: str):
        """
        Retrieves the option which a filter query is currently set to.

        :param query: The filter query being retrieved of its current option
        :return: The option which the filter query is currently set to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__checkboxes:
            elem = self.soup.select(self.__checkboxes[query])[0]
            option = "True" if elem.get("checked") == "checked" else "False"
        elif query in self.__dropdowns:
            elem = self.soup.select(self.__dropdowns[query])[0]
            option = elem.get("value")
        elif query in self.__selections:
            elem = self.soup.select(f"{self.__selections[query]} .rtsLink.rtsSelected")
            option = elem.getText()
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str, *, autoupdate=True):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :param autoupdate: If ``True``, any buttons attached to the filter query will be clicked
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query, option = query.lower(), str(option).lower()
        if query not in self.list_queries():
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        self._close_ad()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        elif query in self.__checkboxes:
            self.__configure_checkbox(query, option)
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        if query in self.__buttons and autoupdate:
            self.__click_button(query)
        self._refresh_parser()

    def __configure_selection(self, query, option):
        """
        Configures a selection-class filter query to an option.

        :param query: The selection-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = [o.lower() for o in self.list_options(query)]
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option) from err
        self.page.click("#LeaderBoard_tsType a[href='#']")
        elem = self.page.query_selector_all(
            f"{self.__selections[query]} li"
        )[index]
        elem.click()

    def __configure_dropdown(self, query, option):
        """
        Configures a dropdown-class filter query to an option.

        :param query: The dropdown-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = [o.lower() for o in self.list_options(query)]
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option) from err
        self.page.hover(
            self.__dropdowns[query]
        )
        elem = self.page.query_selector_all(
            f"{self.__dropdowns[query]} > div > ul > li"
        )[index]
        elem.click()

    def __configure_checkbox(self, query, option):
        """
        Configures a checkbox-class filter query to an option.

        :param query: The checkbox-class filter query to be configured
        :param option: The option to set the filter query to
        """
        options = self.list_options(query)
        if option not in options:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option)
        if option != self.current_option(query).title():
            self.page.click(self.__checkboxes[query])

    def __click_button(self, query):
        """
        Clicks the button element which is attached to the search query.

        :param query: The filter query which has an attached form submission button
        """
        self.page.click(
            self.__buttons[query]
        )

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self.export_data("#LeaderBoard1_cmdCSV", path)


class Splits(utilities.ScrapingUtilities):
    """
    Scrapes the FanGraphs `Splits Leaderboards`_ page.

    .. _Splits Leaderboards: https://fangraphs.com/leaders/splits-leaderboards
    """
    __selections = leaders_sel.Splits.selections
    __dropdowns = leaders_sel.Splits.dropdowns
    __splits = leaders_sel.Splits.splits
    __quick_splits = leaders_sel.Splits.quick_splits
    __switches = leaders_sel.Splits.switches
    __waitfor = leaders_sel.Splits.waitfor

    address = "https://fangraphs.com/leaders/splits-leaderboards"

    def __init__(self, *, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)

        self.configure_filter_group("Show All")
        self.configure("auto_pt", "False", autoupdate=True)

    @classmethod
    def list_queries(cls):
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :rtype: list
        """
        queries = []
        queries.extend(list(cls.__selections))
        queries.extend(list(cls.__dropdowns))
        queries.extend(list(cls.__splits))
        queries.extend(list(cls.__switches))
        return queries

    def list_options(self, query: str):
        """
        Lists the possible options which a filter query can be configured to.

        :param query: The filter query
        :return: Options which the filter query can be configured to
        :rtype: list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__selections:
            elems = [
                self.soup.select(s)[0]
                for s in self.__selections[query]
            ]
            options = [e.getText() for e in elems]
        elif query in self.__dropdowns:
            selector = f"{self.__dropdowns[query]} ul li"
            elems = self.soup.select(selector)
            options = [e.getText() for e in elems]
        elif query in self.__splits:
            selector = f"{self.__splits[query]} ul li"
            elems = self.soup.select(selector)
            options = [e.getText() for e in elems]
        elif query in self.__switches:
            options = ["True", "False"]
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return options

    def current_option(self, query: str):
        """
        Retrieves the option(s) which a filter query is currently set to.

        Most dropdown- and split-class filter queries can be configured to multiple options.
        For those filter classes, a list is returned, while other filter classes return a string.

        - Selection-class: ``str``
        - Dropdown-class: ``list``
        - Split-class: ``list``
        - Switch-class: ``str``

        :param query: The filter query being retrieved of its current option
        :return: The option(s) which the filter query is currently set to
        :rtype: str or list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        option = []
        if query in self.__selections:
            for sel in self.__selections[query]:
                elem = self.soup.select(sel)[0]
                if "isActive" in elem.get("class"):
                    option = elem.getText()
                    break
        elif query in self.__dropdowns:
            elems = self.soup.select(
                f"{self.__dropdowns[query]} ul li"
            )
            for elem in elems:
                if "highlight-selection" in elem.get("class"):
                    option.append(elem.getText())
        elif query in self.__splits:
            elems = self.soup.select(
                f"{self.__splits[query]} ul li"
            )
            for elem in elems:
                if "highlight-selection" in elem.get("class"):
                    option.append(elem.getText())
        elif query in self.__switches:
            elem = self.soup.select(self.__switches[query])
            option = "True" if "isActive" in elem[0].get("class") else "False"
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str, *, autoupdate=False):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :param autoupdate: If ``True``, :py:meth:`update` will be called following configuration
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        self._close_ad()
        query = query.lower()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        elif query in self.__splits:
            self.__configure_split(query, option)
        elif query in self.__switches:
            self.__configure_switch(query, option)
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        if autoupdate:
            self.update()
        self._refresh_parser(waitfor=self.__waitfor)

    def __configure_selection(self, query: str, option: str):
        """
        Configures a selection-class filter query to an option.

        :param query: The selection-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option) from err
        self.page.click(self.__selections[query][index])

    def __configure_dropdown(self, query: str, option: str):
        """
        Configures a dropdown-class filter query to an option.

        :param query: The dropdown-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option) from err
        self.page.hover(self.__dropdowns[query])
        elem = self.page.query_selector_all(f"{self.__dropdowns[query]} ul li")[index]
        elem.click()

    def __configure_split(self, query: str, option: str):
        """
        Configures a split-class filter query to an option.
        Split-class filter queries are separated from dropdown-class filter queries.
        This is solely because of the CSS selectors used.

        :param query: The split-class filter query to be configured
        :param option: The option to configure the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option) from err
        self.page.hover(self.__splits[query])
        elem = self.page.query_selector_all(f"{self.__splits[query]} ul li")[index]
        elem.click()

    def __configure_switch(self, query: str, option: str):
        """
        Configures a switch-class filter query to an option.

        :param query: The switch-class filter query to be configured
        :param option: The option to configure the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        if option not in options:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option)
        if option != self.current_option(query)[0].title():
            self.page.click(self.__switches[query])

    def update(self):
        """
        Clicks the **Update** button of the page.
        All configured filters are submitted and the page is refreshed.

        :raises FanGraphs.exceptions.FilterUpdateIncapability: No filter queries to update
        """
        selector = "#button-update"
        elem = self.page.query_selector(selector)
        if elem is None:
            raise fangraphs.exceptions.exceptions.FilterUpdateIncapability()
        self._close_ad()
        elem.click()
        self._refresh_parser(waitfor=self.__waitfor)

    def list_filter_groups(self):
        """
        Lists the possible groups of filter queries which can be used

        :return: Names of the groups of filter queries
        :rtype: list
        """
        elems = self.soup.select(".fgBin.splits-bin-controller div")
        groups = [e.getText() for e in elems]
        return groups

    def configure_filter_group(self, group="Show All"):
        """
        Configures the available filters to a specified group of filters

        :param group: The name of the group of filters
        """
        selector = ".fgBin.splits-bin-controller div"
        elems = self.soup.select(selector)
        options = [e.getText() for e in elems]
        try:
            index = options.index(group)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterGroup(group) from err
        self._close_ad()
        elem = self.page.query_selector_all(selector)[index]
        elem.click()

    def reset_filters(self):
        """
        Resets filters to the original option(s).
        This does not affect the following filter queries:

        - ``group``
        - ``stat``
        - ``type``
        - ``groupby``
        - ``preset_range``
        - ``auto_pt``
        - ``split_teams``
        """
        selector = "#stack-buttons div[class='fgButton small']:nth-last-child(1)"
        elem = self.page.query_selector(selector)
        if elem is None:
            return
        self._close_ad()
        elem.click()

    @classmethod
    def list_quick_splits(cls):
        """
        Lists all the quick splits which can be used.
        Quick splits allow for the configuration of multiple filter queries at once.

        :return: All available quick splits
        :rtype: list
        """
        return list(cls.__quick_splits)

    def configure_quick_split(self, quick_split: str, autoupdate=True):
        """
        Invokes the configuration of a quick split.
        All filter queries affected by :py:meth:`reset_filters` are reset prior to configuration.
        This action is performed by the FanGraphs API and cannot be prevented.

        :param quick_split: The quick split to invoke
        :param autoupdate: If ``True``, :py:meth:`reset_filters` will be called
        :raises FanGraphs.exceptions.InvalidQuickSplitsException: Invalid argument ``quick_split``
        """
        quick_split = quick_split.lower()
        try:
            selector = self.__quick_splits[quick_split]
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidQuickSplit(quick_split) from err
        self._close_ad()
        self.page.click(selector)
        if autoupdate:
            self.update()

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self.export_data(".data-export", path)


class SeasonStatGrid(utilities.ScrapingUtilities):
    """
    Scrapes the FanGraphs `Season Stat Grid`_ page.

    .. _Season Stat Grid: https://fangraphs.com/leaders/season-stat-grid
    """
    __selections = leaders_sel.SeasonStatGrid.selections
    __dropdowns = leaders_sel.SeasonStatGrid.dropdowns
    __waitfor = leaders_sel.SeasonStatGrid.waitfor

    address = "https://fangraphs.com/leaders/season-stat-grid"

    def __init__(self, *, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)

    @classmethod
    def list_queries(cls):
        """
        Lists the possible filter queries which can be sued to modify search results.

        :return: Filter queries which can be used to modify search results
        :type: list
        """
        queries = []
        queries.extend(list(cls.__selections))
        queries.extend(list(cls.__dropdowns))
        return queries

    def list_options(self, query: str):
        """
        Lists the possible options which a filter query can be configured to.

        :param query: The filter query
        :return: Options which the filter query can be configured to
        :rtyp: list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
        """
        query = query.lower()
        if query in self.__selections:
            elems = [
                self.soup.select(s)[0]
                for s in self.__selections[query]
            ]
            options = [e.getText() for e in elems]
        elif query in self.__dropdowns:
            elems = self.soup.select(
                f"{self.__dropdowns[query]} li"
            )
            options = [e.getText() for e in elems]
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return options

    def current_option(self, query: str):
        """
        Retrieves the option which a filter query is currently configured to.

        :param query: The filter query
        :return: The option which the filter query is currently configured to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
        """
        query = query.lower()
        if query in self.__selections:
            selector = "div[class='fgButton button-green active isActive']"
            elems = self.soup.select(selector)
            option = {
                "stat": elems[0].getText(), "type": elems[1].getText()
            }[query]
        elif query in self.__dropdowns:
            elems = self.soup.select(
                f"{self.__dropdowns[query]} li[class$='highlight-selection']"
            )
            option = elems[0].getText() if elems else "None"
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str):
        """
        Configures a filter query to a specified option.

        :param query: The filter query
        :param option: The option to configure ``query`` to
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        self._close_ad()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        self._refresh_parser(waitfor=self.__waitfor)

    def __configure_selection(self, query: str, option: str):
        """
        Configures a selection-class filter query to a specified option.

        :param query: The filter query
        :param option: The option to configure ``query`` to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option) from err
        self.page.click(self.__selections[query][index])

    def __configure_dropdown(self, query: str, option: str):
        """
        Configures a dropdown-class filter query to a specified option.

        :param query: The filter query
        :param option: The option to configure ``query`` to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option) from err
        self.page.hover(self.__dropdowns[query])
        elem = self.page.query_selector_all(f"{self.__dropdowns[query]} ul li")[index]
        elem.click()

    def _write_table_headers(self, writer: csv.writer):
        """
        Writes the headers of the data table to the CSV file.

        :param writer: The ``csv.writer`` object
        """
        elems = self.soup.select(".table-scroll thead tr th")
        headers = [e.getText() for e in elems]
        writer.writerow(headers)

    def _write_table_rows(self, writer: csv.writer):
        """
        Iterates through the rows of the current data table.
        The data in each row is written to the CSV file.

        :param writer: The ``csv.writer`` object
        """
        row_elems = self.soup.select(".table-scroll tbody tr")
        for row in row_elems:
            elems = row.select("td")
            items = [e.getText() for e in elems]
            writer.writerow(items)

    def export(self, path=""):
        """
        Scrapes and saves the data from the table of the current leaderboards.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *out/%d.%m.%y %H.%M.%S.csv*.

        *Note: This is a 'manual' export of the data.
        In other words, the data is scraped from the table.
        This is unlike other forms of export where a button is clicked.
        Thus, there will be no record of a download when the data is exported.*

        :param path: The path to save the exported file to
        """
        self._close_ad()
        if not path or os.path.splitext(path)[1] != ".csv":
            path = "out/{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        total_pages = int(
            self.soup.select(
                ".table-page-control:nth-last-child(1) > .table-control-total"
            )[0].getText()
        )
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            self._write_table_headers(writer)
            for _ in range(0, total_pages):
                self._write_table_rows(writer)
                self.page.click(
                    ".table-page-control:nth-last-child(1) > .next"
                )
                self._refresh_parser(waitfor=self.__waitfor)


class GameSpan(utilities.ScrapingUtilities):
    """
    Scrapes the FanGraphs `60-Game Span Leaderboards`_ page.

    .. _60-Game Span Leaderboards: https://www.fangraphs.com/leaders/special/60-game-span
    """
    __selections = leaders_sel.GameSpan.selections
    __dropdowns = leaders_sel.GameSpan.dropdowns
    __waitfor = leaders_sel.GameSpan.waitfor

    address = "https://fangraphs.com/leaders/special/60-game-span"

    def __init__(self, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)

    @classmethod
    def list_queries(cls):
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :rtype: list
        """
        queries = []
        queries.extend(list(cls.__selections))
        queries.extend(list(cls.__dropdowns))
        return queries

    def list_options(self, query: str):
        """
        Lists the possible options which a filter query can be configured to.

        :param query: The filter query
        :return: Options which the filter query can be configured to
        :rtype: list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__selections:
            elems = [
                self.soup.select(s)[0]
                for s in self.__selections[query]
            ]
            options = [e.getText() for e in elems]
        elif query in self.__dropdowns:
            elems = self.soup.select(f"{self.__dropdowns[query]} > div > a")
            options = [e.getText() for e in elems]
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return options

    def current_option(self, query: str):
        """
        Retrieves the option which a filter query is currently set to.

        :param query: The filter query being retrieved of its current option
        :return: The option which the filter query is currently set to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        option = ""
        if query in self.__selections:
            for sel in self.__selections[query]:
                elem = self.soup.select(sel)[0]
                if "active" in elem.get("class"):
                    option = elem.getText()
                    break
        elif query in self.__dropdowns:
            elem = self.soup.select(
                f"{self.__dropdowns[query]} > div > span"
            )[0]
            option = elem.getText()
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        self._close_ad()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        self._refresh_parser(waitfor=self.__waitfor)

    def __configure_selection(self, query: str, option: str):
        """
        Configures a selection-class filter query to an option.

        :param query: The selection-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option) from err
        self.page.click(self.__selections[query][index])

    def __configure_dropdown(self, query: str, option: str):
        """
        Configures a dropdown-class filter query to an option.

        :param query: The dropdown-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option) from err
        self.page.click(self.__dropdowns[query])
        elem = self.page.query_selector_all(
            f"{self.__dropdowns[query]} > div > a"
        )[index]
        elem.click()

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self.export_data(".data-export", path)


class International(utilities.ScrapingUtilities):
    """
    Scrapes the FanGraphs `KBO Leaderboards`_ page.

    .. _KBO Leaderboards: https://www.fangraphs.com/leaders/international
    """
    __selections = leaders_sel.International.selections
    __dropdowns = leaders_sel.International.dropdowns
    __checkboxes = leaders_sel.International.checkboxes
    __waitfor = leaders_sel.International.waitfor

    address = "https://www.fangraphs.com/leaders/international"

    def __init__(self, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)

    @classmethod
    def list_queries(cls):
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :rtype: list
        """
        queries = []
        queries.extend(cls.__selections)
        queries.extend(cls.__dropdowns)
        queries.extend(cls.__checkboxes)
        return queries

    def list_options(self, query: str):
        """
        Retrieves the option which a filter query is currently set to.

        :param query: The filter query being retrieved of its current option
        :return: The option which the filter query is currently set to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__selections:
            elems = [
                self.soup.select(s)[0]
                for s in self.__selections[query]
            ]
            options = [e.getText() for e in elems]
        elif query in self.__dropdowns:
            elems = self.soup.select(
                f"{self.__dropdowns[query]} > div > a"
            )
            options = [e.getText() for e in elems]
        elif query in self.__checkboxes:
            options = ["True", "False"]
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return options

    def current_option(self, query: str):
        """

        :param query:
        :return:
        """
        query = query.lower()
        option = ""
        if query in self.__selections:
            for sel in self.__selections[query]:
                elem = self.soup.select(sel)[0]
                if "active" in elem.get("class"):
                    option = elem.getText()
                    break
        elif query in self.__dropdowns:
            elem = self.soup.select(
                f"{self.__dropdowns[query]} > div > span"
            )[0]
            option = elem.getText()
        elif query in self.__checkboxes:
            elem = self.soup.select(
                self.__selections["stat"][0]
            )
            option = "True" if ",to" in elem[0].get("href") else "False"
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        self._close_ad()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        elif query in self.__checkboxes:
            self.__configure_checkbox(query, option)
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        self._refresh_parser(waitfor=self.__waitfor)

    def __configure_selection(self, query: str, option: str):
        """
        Configures a selection-class filter query to an option.

        :param query: The selection-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption from err
        self.page.click(
            self.__selections[query][index]
        )

    def __configure_dropdown(self, query: str, option: str):
        """
        Configures a dropdown-class filter query to an option.

        :param query: The dropdown-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption from err
        self.page.click(self.__dropdowns[query])
        elem = self.page.query_selector_all(
            f"{self.__dropdowns[query]} > div > a"
        )[index]
        elem.click()

    def __configure_checkbox(self, query: str, option: str):
        """
        Configures a checkbox-class filter query to an option.

        :param query: The checkbox-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        if option not in options:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption
        if option == self.current_option(query):
            return
        self.page.click(self.__checkboxes[query])

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self.export_data(".data-export", path)


class WAR(utilities.ScrapingUtilities):
    """
    Scrapes the FanGraphs `Combined WAR Leaderboards`_ page.

    .. _Combined WAR Leaderboards: https://www.fangraphs.com/warleaders.aspx
    """
    __dropdowns = leaders_sel.WAR.dropdowns
    __dropdown_options = leaders_sel.WAR.dropdown_options
    __waitfor = leaders_sel.WAR.waitfor

    address = "https://fangraphs.com/warleaders.aspx"

    def __init__(self, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)

    @classmethod
    def list_queries(cls):
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :rtype: list
        """
        queries = []
        queries.extend(list(cls.__dropdowns))
        return queries

    def list_options(self, query: str):
        """
        Lists the possible options which a filter query can be configured to.

        :param query: The filter query
        :return: Options which the filter query can be configured to
        :rtype: list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__dropdowns:
            elems = self.soup.select(
                f"{self.__dropdown_options[query]} > ul > li"
            )
            options = [e.getText() for e in elems]
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return options

    def current_option(self, query: str):
        """
        Retrieves the option which a filter query is currently set to.

        :param query: The filter query being retrieved of its current option
        :return: The option which the filter query is currently set to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__dropdowns:
            elem = self.soup.select(self.__dropdowns[query])[0]
            option = elem.get("value")
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        self._close_ad()
        if query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        else:
            raise fangraphs.exceptions.exceptions.InvalidFilterQuery(query)
        self._refresh_parser(waitfor=self.__waitfor)

    def __configure_dropdown(self, query: str, option: str):
        """
        Configures a dropdown-class filter query to an option.

        :param query: The dropdown-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.exceptions.InvalidFilterOption(query, option) from err
        self.page.click(self.__dropdowns[query])
        elem = self.page.query_selector_all(
            f"{self.__dropdown_options} > ul > li"
        )[index]
        elem.click()

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self.export_data("#WARBoard1_cmdCSV", path)
