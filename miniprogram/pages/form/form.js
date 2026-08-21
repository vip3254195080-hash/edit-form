Page({
  data: {
    videoTypes: ['AI短剧剪辑', '短视频带货', '宣传片/广告', '达芬奇调色', '音频分离'],
    typeIndex: 0,
    clientName: '',
    contactInfo: '',
    duration: '',
    budget: '',
    materialUrl: '',
    referenceUrl: '',
    notes: '',
    submitting: false
  },
  onTypeChange: function(e) {
    this.setData({ typeIndex: Number(e.detail.value) });
  },
  onInput: function(e) {
    var field = e.currentTarget.dataset.field;
    var update = {};
    update[field] = e.detail.value;
    this.setData(update);
  },
  submitForm: function() {
    var that = this;
    var data = this.data;
    if (!data.clientName.trim() || !data.contactInfo.trim()) {
      wx.showToast({ title: '请填写称呼与联系方式', icon: 'none' });
      return;
    }
    that.setData({ submitting: true });
    wx.request({
      url: 'http://127.0.0.1:8000/api/requirements',
      method: 'POST',
      data: {
        client_name: data.clientName,
        contact_info: data.contactInfo,
        video_type: data.videoTypes[data.typeIndex],
        duration: data.duration || '未填写',
        budget: data.budget || '面议',
        material_url: data.materialUrl,
        reference_url: data.referenceUrl,
        notes: data.notes
      },
      success: function(res) {
        if (res.data && res.data.code === 200) {
          wx.showModal({
            title: '提交成功 🎉',
            content: '需求已成功保存入库！',
            showCancel: false,
            success: function() {
              that.setData({
                clientName: '',
                contactInfo: '',
                duration: '',
                budget: '',
                materialUrl: '',
                referenceUrl: '',
                notes: ''
              });
            }
          });
        } else {
          wx.showToast({ title: '提交失败，请重试', icon: 'none' });
        }
      },
      fail: function() {
        wx.showModal({
          title: '连接后端失败',
          content: '请确认后台已启动：.\\venv\\Scripts\\python.exe -m uvicorn app.main:app --reload --port 8000',
          showCancel: false
        });
      },
      complete: function() {
        that.setData({ submitting: false });
      }
    });
  }
});