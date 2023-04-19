//主文件，对wxChat的用法做示例

<template>
<div>
<wxChat 
  :data="wxChatData"
  :showShade="false"
  contactNickname="乐乐"
  :ownerAvatarUrl="ownerAvatarUrl"
  :contactAvatarUrl="contactAvatarUrl">
</wxChat>
</div>

</template>

<script>
import wxChat from './components/wxChat.vue'

export default {
  name: 'app',
  data () {
    return {
      upperTimes: 0,
      underTimes: 0,
      upperId: 0,
      underId: 6,
      ownerAvatarUrl: './static/owner.png',
      contactAvatarUrl: './static/lele2.png',
      wxChatData: [{
        direction: 2,
        id: 1,
        type: 1,
        content: '你好,乐乐！',
        ctime: new Date().toLocaleString()
      },
      {
        direction: 1,
        id: 2,
        type: 1,
        content: '我在，请讲',
        ctime: new Date().toLocaleString()
      },
      ]
    }
  },
  components:{wxChat},
  created(){
  },
}
</script>

<style>
*{
  margin: 0;
  padding: 0;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
}

</style>
