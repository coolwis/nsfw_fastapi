<template>
  <div class="main">
      <div>AI 모델 활용 부적합  이미지 판정</div>
    <hr/>
    <div
      class="dropzone-container"
      @dragover="dragover"
      @dragleave="dragleave"
      @drop="drop"
    >
      <input
        type="file"
        multiple
        name="file"
        id="fileInput"
        class="hidden-input"
        @change="onChange"
        ref="file"
        accept=".jpg,.jpeg,.png"
      />

      <label for="fileInput" class="file-label">
        <div v-if="isDragging">Release to drop files here.</div>
        <div v-else>Drop files here or <u>click here</u> to upload.</div>
      </label>

      <div class="preview-container mt-4" v-if="files.length">
        <div v-for="file in files" :key="file.name" class="preview-card">
          <div >
            <img style="width: 100px;height:100px;" :src="generateThumbnail(file)" />
            <p :title="file.name">
              {{ makeName(file.name) }}
            </p>
          </div>
          <div>
            <button
              class="ml-2"
              type="button"
              @click="remove(files.indexOf(file))"
              title="Remove file"
            >
              <b>&times;</b>
            </button>
          </div>
        </div>
      </div>
      <hr/>
      <div style="diplay:flex">
         <div> 
            <label v-bind:style="{ color: 'darkgreen', fontSize: '25px' }">{{ "이미지 판정 결과:"}}</label> 
         </div>
          <div v-bind:style="{ color: activeColor, fontSize: '20px' }"> {{ resultMsg }} </div>
      </div>      
      <div>
          <div  v-bind:style="{ color: 'darkgreen', fontSize: '25px' }"> {{ "AI 모델 측정값" }} </div>
          <pre>  {{ JSON.stringify(resultData, null, 2) }} </pre>
      </div>
      <hr/>
      <div>	
          <label v-bind:style="{ color: 'darkgreen', fontSize: '25px' }">{{ "Tech And  Architect"}}</label> 
       
        <div>FrontEnd:<b> Vue.js</b> </div>
        <div>BackEnd: <b>FastApi(Python) </b> </div>
        <div>AI Model: 
            <a href="https://s3.amazonaws.com/ir_public/nsfwjscdn/nsfw_mobilenet2.224x224.h5">
            nsfw_mobilenet2.224x224.h5 </a> 
        </div>
        <div>git url: <a href="https://github.com/coolwis/nsfw_fastapi.git">
          https://github.com/coolwis/nsfw_fastapi.git</a> </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      isDragging: false,
      files: [],
      resultMsg: '', 
      resultData: {},
      isNsfw : false,
      activeColor: 'blue',  
      fileSrc: '',
    };
  },
  mounted() {
    this.initData();
  },
  methods: {
    initData() {
      this.resultData = {
        "drawings": 0,
        "hentai": 0,
        "neutral": 0,
        "porn": 0,
        "sexy": 0,
        }
    },
    onChange() {
      this.files = [...this.$refs.file.files];
	    this.uploadFiles();
    },
    uploadFiles(){
      const that = this; 
      const apiUrl = process.env.VUE_APP_API_URL;
      const uploadUrl = apiUrl+"/fastapi/file/upload/";
      console.log('uploadUrl', uploadUrl);
      // one file
      const file = this.files[0];
      let formData  = new FormData();
      formData.append("file", file);
      // backen: __init__.py 에서 aws url 수정 필요!!
      that.resultMsg = '';
      that.initData();
      that.isNsfw = false;
      that.activeColor ='blue';
      axios( {
        method:"POST",       
        url: uploadUrl,
        data: formData,
        headers : { "Content-Type":"multipart/form-data"},
      })      
      .then(function (response){	    	
          if(response.data.data) {                    
            const img_preds = response.data.data.img_preds;
            console.log('img_preds >>', img_preds);
            let points={};
           
            Object.keys(img_preds).forEach(key => {
                 points= img_preds[key];
            });

            const nsfw1 = Number(points.sexy);
            const nsfw2 =  Number(points.porn);
            console.log('222',  points);
            console.log('nsfw1',  nsfw1);
            console.log('nsfw2',  nsfw2);
            if(nsfw1 > 0.8 || nsfw2 > 0.8) { 
              that.resultMsg='부적합한 이미지로 판정 되었습니다!';			
              that.isNsfw = true;		
              that.activeColor ='red';	
            } else { 
              that.resultMsg= 'Normal Image';
            }
            that.resultData = points;
          }        
      });          
    },

    generateThumbnail(file) {
      let fileSrc = URL.createObjectURL(file);
      setTimeout(() => {
        URL.revokeObjectURL(fileSrc);
      }, 1000);
      return fileSrc;
    },

  
    makeName(name) {
	    if(name.length < 10) return name;
      return (	
        name.split(".")[0].substring(0,10 ) +
        "..." +
        name.split(".")[name.split(".").length - 1]
      );
    },

    remove(i) {
      this.files.splice(i, 1);
    },

    dragover(e) {
      e.preventDefault();
      this.isDragging = true;
    },

    dragleave() {
      this.isDragging = false;
    },

    drop(e) {
      e.preventDefault();
      this.$refs.file.files = e.dataTransfer.files;
      this.onChange();
      this.isDragging = false;
    },
  },
};
</script>

<style>
.main {
  display: flex;
  flex-grow: 1;
  align-items: center;
  height: 100vh;
  justify-content: center;
  text-align: center;
}
.dropzone-container {
  padding: 4rem;
  background: #f7fafc;
  border: 1px solid #e2e8f0;
}
.hidden-input {
  opacity: 0;
  overflow: hidden;
  position: absolute;
  width: 1px;
  height: 1px;
}
.file-label {
  font-size: 20px;
  display: block;
  cursor: pointer;
}
.preview-container {
  display: flex;
  margin-top: 2rem;
}
.preview-card {
  display: flex;
  border: 1px solid #a2a2a2;
  padding: 5px;
  margin-left: 5px;
}
.preview-img {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  border: 1px solid #a2a2a2;
  background-color: #a2a2a2;
}


.title {
  color: blue;
  font-size: 30px;
}
.activeClass {
  font-color: red;
}

