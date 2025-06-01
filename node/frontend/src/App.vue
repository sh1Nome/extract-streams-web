<script setup lang="ts">
import { ref } from "vue";

const file = ref<File | null>(null);

function handleExtractAudio() {
  if (file.value) {
    console.log(file.value.name);
  } else {
    console.log("ファイルが選択されていません");
  }
}
</script>

<template>
  <v-file-input label="File input" v-model="file"></v-file-input>
  <v-btn @click="handleExtractAudio">音声トラックを抽出</v-btn>
</template>
