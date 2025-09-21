<template>
  <!-- TODO: actionのハードコードをやめる -->
  <form
    :action="'http://localhost:8000/api/v1/extract_audio'"
    method="POST"
    enctype="multipart/form-data"
    target="_blank"
  >
    <input type="file" name="file" accept="video/*" required />
    <button type="submit">音声トラックを抽出</button>
  </form>
</template>
