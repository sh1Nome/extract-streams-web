<script setup lang="ts">
import { ref } from "vue";

const file = ref<File | null>(null);

async function handleExtractAudio() {
  if (!file.value) {
    console.log("ファイルが選択されていません");
    return;
  }
  const formData = new FormData();
  formData.append("file", file.value);
  try {
    // TODO: APIのURLを環境変数から取得するように変更
    const response = await fetch("http://localhost:8000/api/v1/extract_audio", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      throw new Error("リクエストに失敗しました");
    }
    // zipファイルのblobを取得
    const blob = await response.blob();
    // ファイル名をContent-Dispositionから取得
    const disposition = response.headers.get("Content-Disposition");
    let filename = "audio.zip";
    if (disposition) {
      const match = disposition.match(/filename="?([^";]+)"?/);
      if (match) filename = match[1];
    }
    // ダウンロード処理
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    console.log("ダウンロード完了");
  } catch (error) {
    console.error("エラー:", error);
  }
}
</script>

<template>
  <v-file-input label="File input" v-model="file"></v-file-input>
  <v-btn @click="handleExtractAudio">音声トラックを抽出</v-btn>
</template>
