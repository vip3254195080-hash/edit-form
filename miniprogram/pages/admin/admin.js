Page({
  data: { list: [] },
  onShow: function() { this.fetchList(); },
  onPullDownRefresh: function() { this.fetchList(); },
  fetchList: function() {
    var that = this;
    wx.request({
      url: 'http://127.0.0.1:8000/api/requirements',
      method: 'GET',
      success: function(res) {
        if (res.data && res.data.code === 200) {
          that.setData({ list: res.data.data });
        }
      },
      complete: function() { wx.stopPullDownRefresh(); }
    });
  },
  copyText: function(e) {
    wx.setClipboardData({
      data: e.currentTarget.dataset.text || '',
      success: function() { wx.showToast({ title: '已复制' }); }
    });
  }
});