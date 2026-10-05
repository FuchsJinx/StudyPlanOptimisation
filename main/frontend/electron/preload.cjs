/** Preload bridge — extend when native APIs are needed. */
const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("studyplan", {
  platform: process.platform,
  versions: process.versions,
});
