//微信聊天可视化组件
//依赖scrollLoader组件, 依赖指令v-emotion（实现请查看main.js）

//参数：
// width 组件宽度，默认450
// wrapBg 外层父元素背景颜色，默认#efefef
// maxHeight 展示窗口最高高度, 默认900
// contactAvatarUrl 好友头像url
// ownerAvatarUrl 微信主人头像url
// ownerNickname 微信主人昵称
// getUpperData （必需）当滚动到上方时加载数据的方法，返回值要为Promise对象，resolve的结构同data
// getUnderData （必需）当滚动到下方时加载数据的方法，返回值同上
// data （必需）传入初始化数据， 结构如下：
[{
direction: 2, //为2表示微信主人发出的消息，1表示联系人
id: 1, //根据这个来排序消息
type: 1, //1为文本，2为图片，3为视频,4为加载中
content: '你好!![呲牙]', //当type为1时这里是文本消息，当type为2时这里要存放图片地址，当type为3时，这里存放视频流
ctime: new Date().toLocaleString() //显示当前消息的发送时间
},
{
direction: 1,
id: 2,
type: 1,
content: '你也好。[害羞]',
ctime: new Date().toLocaleString()
}]


<style scoped>
  .wxchat-container {
    width: 100%;
    height: 100%;
    z-index: 100;
    left: 0;
    top: 0;
    /* overflow: hidden; */
  }

  .shadow {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 100;
    width: 100%;
    height: 100%;
    background: #000;
    opacity: .2;
  }

  .window {
    box-shadow: 1px 1px 20px -5px #000;
    /*max-width: 450px;*/
    min-width: 300px;
    background: #F5F5F5;
    margin: 0 auto;
    overflow: hidden;
    padding: 0;
    height: 100%;
    position: relative;
    z-index: 101;
  }

  .w100 {
    width: 100%;
  }

  .mt5 {
    margin-top: 5px;
  }

  .mt10 {
    margin-top: 10px;
  }

  .mt20 {
    margin-top: 20px;
  }

  .mb10 {
    margin-bottom: 10px;
  }

  .mb20 {
    margin-bottom: 20px;
  }

  .fs0 {
    font-size: 0
  }

  .title {
    background: #000;
    text-align: center;
    color: #fff;
    width: 100%;
    height: 50px;
    line-height: 50px;
    font-size: 14px;
  }

  .input-area {
    background: #fff;
    text-align: center;
    color: #000;
    width: 100%;
    height: 50px;
    line-height: 50px;
    font-size: 14px;
  }

  .loading,
  .no-more {
    text-align: center;
    color: #b0b0b0;
    line-height: 100px;
  }

  .no-more {
    line-height: 60px;
  }

  .pull-right {
    float: right;
  }

  .link-line {
    text-decoration: underline;
  }

  .message {
    /*height: 100%;*/
    padding: 10px 15px;
    /*overflow-y: scroll;*/
    background-color: #F5F5F5;
  }

  .message li {
    margin-bottom: 15px;
    left: 0;
    position: relative;
    display: block;
  }

  .message .time {
    margin: 10px 0;
    text-align: center;
  }

  .message .text {
    display: inline-block;
    position: relative;
    padding: 0 10px;
    max-width: calc(100% - 75px);
    min-height: 35px;
    line-height: 2.1;
    font-size: 15px;
    padding: 6px 10px;
    text-align: left;
    word-break: break-all;
    background-color: #fff;
    color: #000;
    border-radius: 4px;
    box-shadow: 0px 1px 7px -5px #000;
  }

  .message .avatar {
    float: left;
    margin: 0 10px 0 0;
    border-radius: 3px;
    background: #fff;
  }

  .message .time>span {
    display: inline-block;
    padding: 0 5px;
    font-size: 12px;
    color: #fff;
    border-radius: 2px;
    background-color: #DADADA;
  }

  .message .system>span {
    padding: 4px 9px;
    text-align: left;
  }

  .message .text:before {
    content: " ";
    position: absolute;
    top: 9px;
    right: 100%;
    border: 6px solid transparent;
    border-right-color: #fff;
  }

  .message .self {
    text-align: right;
  }

  .message .self .avatar {
    float: right;
    margin: 0 0 0 10px;
  }

  .message .self .text {
    background-color: #9EEA6A;
  }

  .message .self .text .emotion {
    color: #dd0b0b;
    font-size: 14px;
  }

  .message .self .text:before {
    right: inherit;
    left: 100%;
    border-right-color: transparent;
    border-left-color: #9EEA6A;
  }

  .message .image {
    max-width: 200px;
  }

  .message .video {
    max-width: 200px;
  }

  img.static-emotion-gif,
  img.static-emotion {
    vertical-align: middle !important;
  }

  .an-move-left {
    left: 0;
    animation: moveLeft .7s ease;
    -webkit-animation: moveLeft .7s ease;
  }

  .an-move-right {
    left: 0;
    animation: moveRight .7s ease;
    -webkit-animation: moveRight .7s ease;
  }

  .bgnone {
    background: none;
  }

  .box-card {
    margin-bottom: 12px;
  }

  .develop-drawer-padding {
    margin: 15px;
  }
  .el-drawer.rtl{
    width: 70% !important;
  }

  @keyframes moveRight {
    0% {
      left: -20px;
      opacity: 0
    }

    ;

    100% {
      left: 0;
      opacity: 1
    }
  }

  @-webkit-keyframes moveRight {
    0% {
      left: -20px;
      opacity: 0
    }

    ;

    100% {
      left: 0px;
      opacity: 1
    }
  }

  @keyframes moveLeft {
    0% {
      left: 20px;
      opacity: 0
    }

    ;

    100% {
      left: 0px;
      opacity: 1
    }
  }

  @-webkit-keyframes moveLeft {
    0% {
      left: 20px;
      opacity: 0
    }

    ;

    100% {
      left: 0px;
      opacity: 1
    }
  }

  @media (max-width: 367px) {
    .fzDInfo {
      width: 82%;
    }
  }
</style>

<template>
  <div>
    <div class="wxchat-container" :style="{backgroundColor: wrapBg}">
      <div class="gap" :style="{height: gapHeight + 'px'}">
      </div>
      <div class="window" id="window-view-container" :style="{height: maxHeight + 'px', width: width +'px'}">
        <!-- data is empty -->
        <div class="loading" v-if="dataArray && dataArray.length==0">
          <div style="margin-top: 300px;text-align:center; font-size: 16px;">
            <span>未查找到聊天记录</span>
          </div>
        </div>

        <!-- loading -->
        <div class="loading" v-if="dataArray.length==0">
          <div style="margin-top: 300px;">
            <div>加载中...</div>
          </div>
        </div>

        <div class="title" v-if="dataArray && dataArray.length>0">
          <p v-text="contactNickname"></p>
        </div>
        <!-- main -->
        <ScrollLoader :minHeight="minHeight-100" class="container-main" v-if="dataArray && dataArray.length>0"
          :style="{maxHeight: maxHeight-100 + 'px'}">
          <div class="message">
            <ul>
              <li v-for="(message) in dataArray" :key="message.id"
                :class="message.direction==2?'an-move-right':'an-move-left'">
                <!-- <p class="time"> <span v-text="message.ctime"></span> </p> -->
                <p class="time system" v-if="message.type==10000"> <span v-html="message.content"></span> </p>
                <div :class="'main' + (message.direction==2?' self':'')" v-else>
                  <img class="avatar image" width="45" height="45"
                    :src="message.direction==2? ownerAvatarUrl: contactAvatarUrl">
                  <!-- 文本 -->
                  <div class="text" v-emotion="message.content" v-if="message.type==1"></div>

                  <!-- 图片 -->
                  <div class="text" v-else-if="message.type==2">
                    <img :src="message.content" class="image" alt="聊天图片">
                  </div>

                  <!-- 视频 -->
                  <div class="text" v-else-if="message.type==3">
                    <video controls="controls" class="video" :src="message.content"></video>
                  </div>

                  <!-- 加载中 -->
                  <div class="text" v-else-if="message.type==4">
                    <p>分析中。。。</p>
                  </div>

                  <!-- 文本+情感 -->
                  <div class="text" v-else-if="message.type==5">
                    <p v-text="message.content"></p>
                    <p class='emotion' v-text="message.emotion"></p>
                  </div>

                  <!-- 其他 -->
                  <div class="text" v-else-if="message.type!=10000"
                    v-text="'[暂未支持的消息类型:'+ message.type +']\n\r' + message.content">

                  </div>
                </div>
              </li>

            </ul>
          </div>

        </ScrollLoader>
        <div class="input-area">
          <el-input v-model="textInput" :style="{width: '40%'}" placeholder="请输入内容" @keyup.enter.native="massageSend()"
            v-if="inputSelectRadio=='2' || inputSelectRadio=='3'"></el-input>
          <el-button type="success" @click="massageSend()" :style="{width: '20%'}" v-if="inputSelectRadio=='2' || inputSelectRadio=='3'">发送
          </el-button>

          <el-popover placement="top" trigger="manual" v-model="cameraOpen"
            v-if="inputSelectRadio=='1' || inputSelectRadio=='3'">
            <!-- 摄像头预览 -->
            <el-card class="box-card">
              <video id="videoCamera" :width="cameraHeight" :height="cameraHeight" autoplay muted="true"></video>
              <canvas style="display: none" id="canvasCamera" :width="cameraHeight" :height="cameraHeight"></canvas>
            </el-card>

            <div style="text-align: right; margin: 0">
              <el-button type="success" @click="cameraStart()" :style="{width: '25%'}" :disabled="catchOpen">{{fetchButtonText}}</el-button>
              <el-button type="text" @click="cameraCancel()" :style="{width: '25%'}">取消</el-button>
              <el-button type="primary" @click="cameraSend()" :style="{width: '25%'}">发送</el-button>
            </div>
            <el-button type="primary" slot="reference" :style="{width: '20%'}" @click="cameraOption()"
              :disabled="cameraOpen">视频</el-button>
          </el-popover>
        </div>
      </div>
      <div class="gap" :style="{height: gapHeight + 'px'}">
      </div>
    </div>
    <div class="detail-container">

      <el-button @click="detailDrawer = true" type="info" style="margin-left: 16px;" plain>
        开发者面板
      </el-button>

      <el-drawer title="开发者面板" :visible.sync="detailDrawer" :direction="drawerDirection" :with-header="true">
        <div class="develop-drawer-padding">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>输入方式</span>
            </div>
            <el-radio v-model="inputSelectRadio" label="1">视频</el-radio>
            <el-radio v-model="inputSelectRadio" label="2">文本</el-radio>
            <el-radio v-model="inputSelectRadio" label="3">视频+文本</el-radio>
          </el-card>
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>对话模型情绪选择</span>
            </div>
            <el-radio v-model="replyEmotionSelectRadio" label="1">普通</el-radio>
            <el-radio v-model="replyEmotionSelectRadio" label="2">高兴</el-radio>
            <el-radio v-model="replyEmotionSelectRadio" label="3">忧郁</el-radio>
            <el-radio v-model="replyEmotionSelectRadio" label="4" disabled>暴躁</el-radio>
            <el-radio v-model="replyEmotionSelectRadio" label="5" disabled>厌恶</el-radio>
          </el-card>
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>对话模型选择</span>
            </div>
            <el-radio v-model="dialogueModelSelectRadio" label="1">CDial-GPT</el-radio>
            <el-radio v-model="dialogueModelSelectRadio" label="2" disabled>other</el-radio>
          </el-card>
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>多模态情感分析模型选择</span>
            </div>
            <el-radio v-model="multiModelSelectRadio" label="1">Sparse_MME2E</el-radio>
            <el-radio v-model="multiModelSelectRadio" label="2" disabled>E2EMMT_Interact</el-radio>
            <el-radio v-model="multiModelSelectRadio" label="3" disabled>other</el-radio>
          </el-card>

          <el-divider></el-divider>

          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>分析结果</span>
            </div>
            <span>{{analysis_result}}</span>
          </el-card>
          
        </div>
      </el-drawer>
    </div>
  </div>

</template>



<script>
  import ScrollLoader from './scrollLoader.vue';
  import axios from "axios";
  export default {
    name: "wxChat",

    components: {
      ScrollLoader
    },

    props: {
      contactNickname: {
        type: String,
        default: 'Mystic Faces'
      },

      data: {
        type: Array,
        required: true
      },

      wrapBg: {
        type: String,
        default: '#ffffff'
      },

      contactAvatarUrl: {
        type: String,
      },

      ownerAvatarUrl: {
        type: String,
      },
    },

    data() {
      return {

        userID: 0,
        isUpperLaoding: false,
        isUnderLaoding: false,

        isRefreshedAll: false,
        isLoadedAll: false,

        minHeight: 0,
        maxHeight: 0,
        width: 0,
        isMobile: false,
        gapHeight: 0,
        dataArray: [],
        alwaysFalse: false,

        textInput: '',
        cameraOpen: false,
        fetchStart: false,
        fetchButtonText: '录制',
        cameraHeight: 10,

        catchOpen: false,
        thisCancas: null,
        thisContext: null,
        thisVideo: null,
        recordedBlobs: [],
        mediaRecorder: null,

        detailDrawer: false,
        drawerDirection: null,
        inputSelectRadio: "3",
        multiModelSelectRadio: "1",
        dialogueModelSelectRadio: "1",
        analysis_result: '将来可以查看文本，图片分析的具体细节',

        replyEmotionSelectRadio:'1',
        emotionMap:{
          '1':'n',
          '2':'h',
          '3':'s',
          '4':'a',
          '5':'d',
        },
        webUrl: "https://qx.8wss.com/lele",
        videoModelUrl: null,
      }
    },
    watch: {
      replyEmotionSelectRadio(newValue,oldValue){
        console.log(this.emotionMap[this.replyEmotionSelectRadio],)
      },
      dataArray:{
        handler(newValue,oldValue){
          var ele = document.getElementById("scrollLoader-container");
          setTimeout(function(){
            if(ele.scrollHeight > ele.clientHeight) {
              ele.scrollTop = ele.scrollHeight;
            }
          },100);
        },
        deep:true,
      },
      multiModelSelectRadio(newValue,oldValue){
        if (newValue=='1') {
          this.videoModelUrl=this.webUrl+'/sc';
          console.log(this.videoModelUrl);
        }
        if (newValue=='2') {
          this.videoModelUrl=this.webUrl+'/e2emmt';
          console.log(this.videoModelUrl);
        }
      }
    },

    created() {
      this.initData();
    },
    mounted() {
      //document.getElementsByTagName('body')[0].scrollTop=0;
      
      //生成用户时间戳
      let time = new Date();
      let month = time.getMonth() + 1,
        date = time.getDate(),
        h = time.getHours(),
        m = time.getMinutes(),
        s = time.getSeconds();
      this.userID = month + "_" + date + "_" + h + m + s;
      console.log("time is :" + this.userID);


      let url=this.videoModelUrl+'/video_look/'
      console.log(url);
      axios
        .post(url, {},{
          headers: {
            "userid": this.userID,
          },
        },)
        .then((response) => {
          let res = response.data;
          console.log(res);
        });
      
      url=this.webUrl+'/reply/reply_look/'
      console.log(url);
      axios
        .post(url, {},{
          headers: {
            "userid": this.userID,
          },
        },)
        .then((response) => {
          let res = response.data;
          console.log(res);
        });
    },

    methods: {
      initData() {
        this.minHeight = window.innerHeight * 0.85 ;
        this.maxHeight = window.innerHeight * 0.85 ; 
        this.gapHeight = window.innerHeight * 0.04;
        this.width = window.innerWidth;
        this.dataArray = this.dataArray.concat(this.data);
        this.videoModelUrl=this.webUrl+'/sc';
        var ua = navigator.userAgent;
        var ipad = ua.match(/(iPad).*OS\s([\d_]+)/),
        isIphone =!ipad && ua.match(/(iPhone\sOS)\s([\d_]+)/),
        isAndroid = ua.match(/(Android)\s+([\d.]+)/);
        this.isMobile = isIphone || isAndroid;
        //非移动端设置600px宽度，移动端是100%
        if(!this.isMobile){
          this.width = window.innerWidth *0.5;
          this.cameraHeight = this.maxHeight * 0.5;
          this.drawerDirection ='rtl';
        }
        else{
          this.width=window.innerWidth *0.9
          this.cameraHeight = this.width * 0.7;
          this.drawerDirection ='btt';

        }
        },
      //开始录制
      cameraOption() {
        this.fetchButtonText='录制';
        if (this.cameraOpen == false) {
          this.getCompetence();
          this.cameraOpen = true;
          this.catchOpen=false;
        }
      },
      cameraStart() {
        this.recordedBlobs = [];
        this.notification("开始录制");
        this.mediaRecorder.start();
        this.fetchStart = true;
        this.catchOpen=true;

        this.endFetchTime=new Date(new Date().getTime()+8000)
        console.log(this.endFetchTime)
        this.countToFinish()
  

      },
      countToFinish(){
        //录制6s后自动结束
        var _this=this;
        let nowTime=new Date();
        if (nowTime.getTime()>_this.endFetchTime.getTime()){
          if (this.fetchStart == true) {
            this.mediaRecorder.stop();
            this.notification("自动结束录制");
            this.fetchStart = false;
          }
          this.thisVideo.srcObject = null;
          this.cameraOpen = false;
          return;
        }
        else{
          if(this.fetchStart==true){
              let lefttime = parseInt((_this.endFetchTime.getTime() - nowTime.getTime()) / 1000);
              let s = parseInt(lefttime % 60);
              setTimeout(function(){
                _this.fetchButtonText=s;
                console.log(s);
              }, 100);
              setTimeout(function(){
                _this.countToFinish();
              }, 900);
          }
          else{
          }
        }
      },
      cameraCancel() {
        if (this.fetchStart == true) {
          this.mediaRecorder.pause();
          this.notification("录制取消");
          this.fetchStart = false;
        }
        this.thisVideo.srcObject = null;
        this.cameraOpen = false;
      },
      cameraSend() {
        if (this.fetchStart == true) {
          this.mediaRecorder.stop();
          this.fetchStart = false;
        } else {
          this.notification("您没有开始录制");
        }
        this.thisVideo.srcObject = null;
        this.cameraOpen = false;
      },
      //发送文字消息
      massageSend(){
        if (this.textInput != '' ){
          let massage=this.textInput;
          let newId = this.dataArray.length + 1;
          let newMessage = {
            direction: 2, 
            id: newId,
            type: 1, //文本信息
            content: massage,
            ctime: new Date().toLocaleString()
          };
          this.dataArray.push(newMessage);
          this.textInput='';
          axios
          .post(this.webUrl+'/reply/send_text_and_reply_generate/', {
            'massage':massage,
            'emotion':this.emotionMap[this.replyEmotionSelectRadio],
            },{
            headers: {
              "userid": this.userID,
            },
          },)
          .then((response) => {
            let res = response.data;
            console.log(res);
            if (res.error_num === 0) {
              let data = res["data"];
              let content= data['reply'];

              let newId = this.dataArray.length + 1;
              let newMessage = {
                direction: 1, //来自机器人
                id: newId,
                type: 1, //文本信息
                content: content,
                ctime: new Date().toLocaleString()
              };
              this.dataArray.push(newMessage);
            } else {
              console.log(res["msg"]);
            }
          });
        }
      },
      //   初始化摄像头，麦克风；获取权限
      getCompetence() {
        var _this = this;
        _this.thisCancas = document.getElementById("canvasCamera");
        _this.thisContext = _this.thisCancas.getContext("2d");
        _this.thisVideo = document.getElementById("videoCamera");
        // 旧版本浏览器可能根本不支持mediaDevices，我们首先设置一个空对象
        if (navigator.mediaDevices === undefined) {
          navigator.mediaDevices = {};
        }
        // 一些浏览器实现了部分mediaDevices，我们不能只分配一个对象
        // 使用getUserMedia，因为它会覆盖现有的属性。
        // 这里，如果缺少getUserMedia属性，就添加它。
        if (navigator.mediaDevices.getUserMedia === undefined) {
          navigator.mediaDevices.getUserMedia = function (constraints) {
            // 首先获取现存的getUserMedia(如果存在)
            var getUserMedia =
              navigator.webkitGetUserMedia ||
              navigator.mozGetUserMedia ||
              navigator.getUserMedia;
            // 有些浏览器不支持，会返回错误信息
            // 保持接口一致
            if (!getUserMedia) {
              _this.notification('getUserMedia is not implemented in this browser');
              return Promise.reject(
                new Error("getUserMedia is not implemented in this browser")
              );
            }
            // 否则，使用Promise将调用包装到旧的navigator.getUserMedia
            return new Promise(function (resolve, reject) {
              getUserMedia.call(navigator, constraints, resolve, reject);
            });
          };
        }
        var constraints = {
          audio: true,
          video: {
            width: this.cameraHeight,
            height: this.cameraHeight,
            transform: "scaleX(-1)",
          },
        };
        navigator.mediaDevices
          .getUserMedia(constraints)
          .then(function (stream) {
            // 旧的浏览器可能没有srcObject
            if ("srcObject" in _this.thisVideo) {
              _this.thisVideo.srcObject = stream;
              var options = {
                mimeType: 'video/webm'
              };
              console.log(MediaRecorder.isTypeSupported('video/webm'));
              _this.mediaRecorder = new MediaRecorder(stream, options);
              console.log('获得媒体权限');

              _this.mediaRecorder.ondataavailable = (event) => {
                if (event.data && event.data.size > 0) {
                  _this.recordedBlobs.push(event.data);
                }
              }
              _this.mediaRecorder.onstop = (event) => {
                let blob = new Blob(_this.recordedBlobs, {
                  "type": 'video/webm'
                });
                console.log('生成预览');
                let url = URL.createObjectURL(blob);

                let newId = _this.dataArray.length + 1;
                let newMessage = {
                  direction: 2, //来自用户
                  id: newId,
                  type: 3, //视频信息
                  content: url,
                  ctime: new Date().toLocaleString()
                };
                _this.dataArray.push(newMessage);
                newMessage = {
                  direction: 2, //来自用户
                  id: newId + 1,
                  type: 4, //正在加载
                  content: null,
                  emotion: null,
                  ctime: new Date().toLocaleString()
                };
                _this.dataArray.push(newMessage);
                console.log('生成文件');
                let file = new File(_this.recordedBlobs, 'video.webm', {
                  'type': 'video/webm'
                });
                _this.recordFile = file;
                _this.recordedBlobs = [];
                _this.updateFile_Analysis_Reply(file);

                stream.getTracks()[0].stop()
                stream.getTracks()[1].stop()
              }
            } else {
              // 避免在新的浏览器中使用它，因为它正在被弃用。
              _this.thisVideo.src = window.URL.createObjectURL(stream);
            }
            _this.thisVideo.onloadedmetadata = function (e) {
              _this.thisVideo.play();
            };
          })
          .catch((err) => {
            console.log(err);
          });
      },
      async updateFile_Analysis_Reply(file){
        this.updateFile(file).then(result => {
          if (result != ''){
            this.reply_generate(result);
          } 
    })
      },
      // 上传加分析
      async updateFile(file) {
        let old_date = new Date();
        let fd = new FormData();
        fd.append('file', file);
        this.notification('请稍等片刻');
        var text;
        console.log(this.videoModelUrl+'/video_upload/');
        await axios
          .post(this.videoModelUrl+'/video_upload/', fd, {
            headers: {
              "Content-Type": "multipart/form-data",
              "userid": this.userID,
            },
          })
          .then((response) => {
            let res = response.data;
            console.log(res);
            if (res.error_num == 0) {
              let data = res["data"];
              let emotion = parseInt(data["emotion"]);
              text = data["text"];
              let emotion_text = data["emotion_text"];

              let loadingContent = this.dataArray[this.dataArray.length - 1];
              loadingContent.type = 5;
              loadingContent.content = text;
              loadingContent.emotion = "( emotion: " + emotion_text + " )";
            } else {
              let msg = res["msg"];
              const h = this.$createElement;
              let loadingContent = this.dataArray[this.dataArray.length - 1];
              loadingContent.type = 5;
              loadingContent.content = '(无)';
              text=''
              this.$notify({
                title: "错误！",
                message: h("i", {
                  style: "color: teal"
                }, msg),
                duration: 5000,
              });
              
            }
          });
          let new_date = new Date();
          let cost_time=(new_date-old_date)/1000;
          console.log('cost_time:' + cost_time);
          return new Promise((resolve, reject) => {
                resolve(text);
            }
          );
      },
      //生成回复
      reply_generate(massage) {
        axios
          .post(this.webUrl+'/reply/reply_generate/', {
            'massage':massage,
            'emotion':this.emotionMap[this.replyEmotionSelectRadio],
            },{
            headers: {
              "userid": this.userID,
            },
          },)
          .then((response) => {
            let res = response.data;
            console.log(res);
            if (res.error_num === 0) {
              let data = res["data"];
              let content= data['reply'];

              let newId = this.dataArray.length + 1;
              let newMessage = {
                direction: 1, //来自机器人
                id: newId,
                type: 1, //文本信息
                content: content,
                ctime: new Date().toLocaleString()
              };
              this.dataArray.push(newMessage);
            } else {
              console.log(res["msg"]);
            }
          });
      },
      //展示通知消息
      notification(massage) {
        const h = this.$createElement;
        this.$notify({
          message: h("i", {
            style: "color: teal"
          }, massage),
          duration: 4000,
        });
      },

    }
  }
</script>