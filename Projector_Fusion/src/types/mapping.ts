import * as THREE from 'three';

export interface LensConfig {
  id: string;
  throwMin: number;
  throwMax: number;
  fixed: boolean;
  shiftV: [number, number];
  shiftH: [number, number];
}

export interface ProjectorConfig {
  name: string;
  brand: string;
  lumens: number;
  resolution: string;
  nativeAspect: number;
  defaultLens: string;
  compatibleLenses: string[];
}

export interface Projector {
  id: number;
  config: ProjectorConfig;
  group: THREE.Group;
  camera: THREE.PerspectiveCamera;
  mesh: THREE.Mesh;
  target: THREE.Mesh;
  helper: THREE.LineSegments;
  shadowLight: THREE.SpotLight;
  depthRenderTarget: THREE.WebGLRenderTarget;
  depthCamera: THREE.PerspectiveCamera;
  rtPreview: THREE.WebGLRenderTarget | null;
  
  // Lens settings
  currentLensId: string;
  currentLens: LensConfig;
  throwRatio: number;
  lensShiftV: number;
  lensShiftH: number;
  
  // Projection settings
  projDistance: number;
  frustumFar: number;
  projectionIntensity: number;
  projectionTexture: THREE.Texture | null;
  orientation: 'portrait' | 'landscape';
  
  // Keystone
  keystoneV: number;
  keystoneH: number;
  keystoneTLX: number;
  keystoneTLY: number;
  keystoneTRX: number;
  keystoneTRY: number;
  keystoneBLX: number;
  keystoneBLY: number;
  keystoneBRX: number;
  keystoneBRY: number;
  
  // Soft edge
  softEdgeL: number;
  softEdgeR: number;
  softEdgeT: number;
  softEdgeB: number;
  softEdgeGamma: number;
  
  // Lock states
  targetLocked: boolean;
  userMovedTarget: boolean;
  
  // Measurement sprites
  spriteWidth?: THREE.Sprite;
  spriteHeight?: THREE.Sprite;
  spriteTR?: THREE.Sprite;
  spriteInfo?: THREE.Sprite;
}

export interface Camera3D {
  id: number;
  name: string;
  group: THREE.Group;
  camera: THREE.PerspectiveCamera;
  helper: THREE.CameraHelper;
  target: THREE.Mesh;
  mesh: THREE.Mesh;
  
  // Settings
  fov: number;
  near: number;
  far: number;
  aspect: number;
  
  // For export/viewer assignment
  assignedToViewer: boolean;
  assignedToProjectorView: boolean;
  assignedToMappingPreview: boolean;
}

export interface SceneObject {
  id: number;
  name: string;
  type: 'primitive' | 'model' | 'wall' | 'screen';
  mesh: THREE.Object3D;
  visible: boolean;
}

export interface TimelineKeyframe {
  time: number;
  property: 'position' | 'rotation' | 'scale';
  value: THREE.Vector3 | THREE.Euler;
  easing: 'linear' | 'easeIn' | 'easeOut' | 'easeInOut';
}

export interface TimelineLayer {
  id: number;
  objectId: number;
  objectType: 'projector' | 'camera' | 'object';
  name: string;
  keyframes: TimelineKeyframe[];
  visible: boolean;
  locked: boolean;
  color: string;
}

export interface Timeline {
  duration: number;
  currentTime: number;
  playing: boolean;
  fps: number;
  layers: TimelineLayer[];
}

export interface RecordingState {
  isRecording: boolean;
  mediaRecorders: MediaRecorder[];
  recordedBlobs: {
    projector: Blob | null;
    main: Blob | null;
  };
}

export interface ExportSettings {
  resolution: 'preview' | '1080p' | '4k';
  fps: number;
  format: 'png' | 'webm';
  includeProjectorView: boolean;
  includeMainView: boolean;
}

export type TransformMode = 'translate' | 'rotate' | 'scale';
export type GizmoSpace = 'world' | 'local';

export interface Selection {
  type: 'projector' | 'camera' | 'object' | 'target' | null;
  object: THREE.Object3D | null;
  instance: Projector | Camera3D | SceneObject | null;
}
