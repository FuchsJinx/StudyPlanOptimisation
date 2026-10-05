/// <reference types="vite/client" />

interface StudyPlanBridge {
  platform: string;
  versions: NodeJS.ProcessVersions;
}

interface Window {
  studyplan?: StudyPlanBridge;
}
