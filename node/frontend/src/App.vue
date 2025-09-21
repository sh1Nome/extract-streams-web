<template>
  <!-- TODO: actionのハードコードをやめる -->
  <v-container class="d-flex justify-center align-center" style="height: 100vh">
    <v-form
      :action="'http://localhost:8000/api/v1/extract_audio'"
      method="POST"
      enctype="multipart/form-data"
      target="_blank"
      style="width: 400px"
    >
      <v-file-input
        name="file"
        accept="video/*"
        label="動画ファイルを選択"
        required
        prepend-icon="mdi-video"
        variant="outlined"
      ></v-file-input>
      <v-btn type="submit" color="primary" class="mt-4" block>
        音声トラックを抽出
      </v-btn>
    </v-form>
  </v-container>
</template>
