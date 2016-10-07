from PyQt5.QtWidgets import QWidget
from TriblerGUI.defs import PAGE_CHANNEL_DETAILS
from TriblerGUI.home_recommended_item import HomeRecommendedChannelItem, HomeRecommendedTorrentItem
from TriblerGUI.loading_list_item import LoadingListItem
from TriblerGUI.tribler_request_manager import TriblerRequestManager


class HomePage(QWidget):

    def initialize_home_page(self):
        self.window().home_page_table_view.cellClicked.connect(self.on_home_page_item_clicked)

        self.window().home_tab.initialize()
        self.window().home_tab.clicked_tab_button.connect(self.clicked_tab_button)

    def load_popular_torrents(self):
        self.recommended_request_mgr = TriblerRequestManager()
        self.recommended_request_mgr.perform_request("torrents/random", self.received_popular_torrents)

    def clicked_tab_button(self, tab_button_name):
        self.window().home_page_table_view.clear()
        self.window().home_page_table_view.setCellWidget(0, 1, LoadingListItem(self))

        if tab_button_name == "home_tab_channels_button":
            self.recommended_request_mgr = TriblerRequestManager()
            self.recommended_request_mgr.perform_request("channels/popular", self.received_popular_channels)
        elif tab_button_name == "home_tab_torrents_button":
            self.recommended_request_mgr = TriblerRequestManager()
            self.recommended_request_mgr.perform_request("torrents/random", self.received_popular_torrents)

    def received_popular_channels(self, result):
        self.show_channels = True

        if len(result["channels"]) == 0:
            self.window().home_page_table_view.clear()
            self.window().home_page_table_view.setCellWidget(0, 1, LoadingListItem(self, label_text="No recommended channels"))
            return

        cur_ind = 0
        for channel in result["channels"]:
            widget_item = HomeRecommendedChannelItem(self, channel)
            self.window().home_page_table_view.setCellWidget(cur_ind % 3, cur_ind / 3, widget_item)
            cur_ind += 1

    def received_popular_torrents(self, result):
        self.show_channels = False
        self.window().resizeEvent(None)

        if len(result["torrents"]) == 0:
            self.window().home_page_table_view.clear()
            self.window().home_page_table_view.setCellWidget(0, 1, LoadingListItem(self, label_text="No recommended torrents"))
            return

        cur_ind = 0
        for torrent in result["torrents"]:
            widget_item = HomeRecommendedTorrentItem(self, torrent)
            self.window().home_page_table_view.setCellWidget(cur_ind % 3, cur_ind / 3, widget_item)
            cur_ind += 1

    def on_home_page_item_clicked(self, row, col):
        if self.show_channels:
            channel_info = self.window().home_page_table_view.cellWidget(row, col).channel_info
            self.window().channel_page.initialize_with_channel(channel_info)
            self.window().navigation_stack.append(self.window().stackedWidget.currentIndex())
            self.window().stackedWidget.setCurrentIndex(PAGE_CHANNEL_DETAILS)
