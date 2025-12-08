import { useEffect, useRef, useState, useCallback } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { TransformControls } from 'three/examples/jsm/controls/TransformControls.js';
import { 
  Projector, 
  Camera3D, 
  SceneObject, 
  Selection, 
  TransformMode,
  Timeline,
  RecordingState
} from '@/types/mapping';
import { LENSES, PROJECTOR_DATABASE, throwToFOV } from '@/lib/projectorDatabase';

const ASPECT = 16 / 9;
const PROJECTOR_CAMERA_FAR = 500;

interface UseSceneManagerProps {
  containerRef: React.RefObject<HTMLDivElement>;
}

interface SceneManager {
  scene: THREE.Scene | null;
  camera: THREE.PerspectiveCamera | null;
  renderer: THREE.WebGLRenderer | null;
  projectors: Projector[];
  cameras: Camera3D[];
  objects: SceneObject[];
  selection: Selection;
  transformMode: TransformMode;
  contentTexture: THREE.Texture | null;
  contentVideo: HTMLVideoElement | null;
  timeline: Timeline;
  recording: RecordingState;
  projectorViewCamera: Camera3D | null;
  mappingPreviewCamera: Camera3D | null;
  
  // Actions
  addProjector: (modelId: string, withTestPattern?: boolean) => Projector;
  addCamera: () => Camera3D;
  addPrimitive: (type: 'box' | 'plane' | 'sphere' | 'cylinder' | 'cone') => SceneObject;
  addWall: () => SceneObject;
  addTestPattern: (projector: Projector) => SceneObject;
  selectObject: (obj: THREE.Object3D | null) => void;
  setTransformMode: (mode: TransformMode) => void;
  loadContent: (file: File) => Promise<void>;
  setCameraView: (view: 'top' | 'front' | 'left' | 'right' | 'back' | 'perspective') => void;
  deleteSelected: () => void;
  updateProjectorSettings: (projectorId: number, settings: Partial<Projector>) => void;
  updateCameraSettings: (cameraId: number, settings: Partial<Camera3D>) => void;
  assignCameraToProjectorView: (cameraId: number, assigned: boolean) => void;
  assignCameraToMappingPreview: (cameraId: number, assigned: boolean) => void;
  renderToCanvas: (canvas: HTMLCanvasElement, cam: THREE.Camera, width: number, height: number) => void;
  getActiveProjector: () => Projector | null;
  toggleGrid: () => void;
  setProjectorOrientation: (projectorId: number, orientation: 'portrait' | 'landscape') => void;
}

export const useSceneManager = ({ containerRef }: UseSceneManagerProps): SceneManager => {
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const orbitControlsRef = useRef<OrbitControls | null>(null);
  const transformControlsRef = useRef<TransformControls | null>(null);
  const gridHelperRef = useRef<THREE.GridHelper | null>(null);
  const axesHelperRef = useRef<THREE.AxesHelper | null>(null);
  const raycasterRef = useRef<THREE.Raycaster>(new THREE.Raycaster());
  const mouseRef = useRef<THREE.Vector2>(new THREE.Vector2());
  
  const [projectors, setProjectors] = useState<Projector[]>([]);
  const [cameras, setCameras] = useState<Camera3D[]>([]);
  const [objects, setObjects] = useState<SceneObject[]>([]);
  const [selection, setSelection] = useState<Selection>({ type: null, object: null, instance: null });
  const [transformMode, setTransformModeState] = useState<TransformMode>('translate');
  const [contentTexture, setContentTexture] = useState<THREE.Texture | null>(null);
  const [contentVideo, setContentVideo] = useState<HTMLVideoElement | null>(null);
  const [gridVisible, setGridVisible] = useState(true);
  const [projectorViewCamera, setProjectorViewCamera] = useState<Camera3D | null>(null);
  const [mappingPreviewCamera, setMappingPreviewCamera] = useState<Camera3D | null>(null);
  
  const [timeline] = useState<Timeline>({
    duration: 30,
    currentTime: 0,
    playing: false,
    fps: 30,
    layers: [],
  });
  
  const [recording] = useState<RecordingState>({
    isRecording: false,
    mediaRecorders: [],
    recordedBlobs: { projector: null, main: null },
  });

  const projectorIdCounter = useRef(0);
  const cameraIdCounter = useRef(0);
  const objectIdCounter = useRef(0);

  // Initialize scene
  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0f14);
    sceneRef.current = scene;

    // Camera
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.set(15, 10, 15);
    cameraRef.current = camera;

    // Renderer
    const renderer = new THREE.WebGLRenderer({ 
      antialias: true, 
      preserveDrawingBuffer: true,
      alpha: true
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Orbit Controls
    const orbitControls = new OrbitControls(camera, renderer.domElement);
    orbitControls.enableDamping = true;
    orbitControls.dampingFactor = 0.05;
    orbitControlsRef.current = orbitControls;

    // Transform Controls
    const transformControls = new TransformControls(camera, renderer.domElement);
    transformControls.addEventListener('dragging-changed', (event) => {
      orbitControls.enabled = !(event as any).value;
    });
    // TransformControls extends Object3D but TypeScript may not recognize it
    const transformControlsObj = transformControls.getHelper();
    scene.add(transformControlsObj);
    transformControlsRef.current = transformControls;

    // Grid Helper
    const gridHelper = new THREE.GridHelper(100, 100, 0x444444, 0x222222);
    scene.add(gridHelper);
    gridHelperRef.current = gridHelper;

    // Axes Helper
    const axesHelper = new THREE.AxesHelper(5);
    scene.add(axesHelper);
    axesHelperRef.current = axesHelper;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 20, 10);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    scene.add(directionalLight);

    // Update camera helpers in animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      orbitControls.update();
      renderer.render(scene, camera);
    };
    animate();

    // Raycasting for selection
    const handleClick = (event: MouseEvent) => {
      if (!containerRef.current || !cameraRef.current || !sceneRef.current) return;
      if (transformControlsRef.current?.dragging) return;
      
      const rect = containerRef.current.getBoundingClientRect();
      mouseRef.current.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouseRef.current.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      
      raycasterRef.current.setFromCamera(mouseRef.current, cameraRef.current);
      
      // Get all selectable objects
      const selectables: THREE.Object3D[] = [];
      sceneRef.current.traverse((child) => {
        if (child instanceof THREE.Mesh && child.userData && 
            (child.userData.isProjector || child.userData.isCamera || child.userData.isTarget || child.userData.objectId)) {
          selectables.push(child);
        }
      });
      
      const intersects = raycasterRef.current.intersectObjects(selectables, false);
      
      if (intersects.length > 0) {
        const hit = intersects[0].object;
        // Emit custom event for selection
        const customEvent = new CustomEvent('scene-object-clicked', { detail: hit });
        containerRef.current.dispatchEvent(customEvent);
      }
    };
    
    container.addEventListener('click', handleClick);

    // Handle resize
    const handleResize = () => {
      if (!containerRef.current) return;
      const w = containerRef.current.clientWidth;
      const h = containerRef.current.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      container.removeEventListener('click', handleClick);
      renderer.dispose();
      container.removeChild(renderer.domElement);
    };
  }, [containerRef]);

  // Create projector helper
  const createProjectorHelper = useCallback((projector: Projector): THREE.LineSegments => {
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(24 * 3);
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    
    const material = new THREE.LineBasicMaterial({ 
      color: 0x0d9488,
      depthTest: true,
      depthWrite: false
    });
    
    const helper = new THREE.LineSegments(geometry, material);
    helper.matrixAutoUpdate = false;
    
    return helper;
  }, []);

  // Update projector helper geometry
  const updateProjectorHelper = useCallback((projector: Projector) => {
    if (!projector.helper) return;
    
    const { throwRatio, lensShiftV, lensShiftH, projDistance, camera: projCam, group } = projector;
    const aspect = projector.orientation === 'portrait' ? 9 / 16 : 16 / 9;
    
    const fov = throwToFOV(throwRatio);
    const near = 0.1;
    const far = projDistance;
    
    const halfHeight = Math.tan((fov * Math.PI / 180) / 2);
    const halfWidth = halfHeight * aspect;
    
    const shiftV = (lensShiftV / 100) * 2;
    const shiftH = (lensShiftH / 100) * 2;
    
    const nearCorners = [
      new THREE.Vector3(-halfWidth * near + shiftH * near, -halfHeight * near + shiftV * near, -near),
      new THREE.Vector3(halfWidth * near + shiftH * near, -halfHeight * near + shiftV * near, -near),
      new THREE.Vector3(halfWidth * near + shiftH * near, halfHeight * near + shiftV * near, -near),
      new THREE.Vector3(-halfWidth * near + shiftH * near, halfHeight * near + shiftV * near, -near),
    ];
    
    const farCorners = [
      new THREE.Vector3(-halfWidth * far + shiftH * far, -halfHeight * far + shiftV * far, -far),
      new THREE.Vector3(halfWidth * far + shiftH * far, -halfHeight * far + shiftV * far, -far),
      new THREE.Vector3(halfWidth * far + shiftH * far, halfHeight * far + shiftV * far, -far),
      new THREE.Vector3(-halfWidth * far + shiftH * far, halfHeight * far + shiftV * far, -far),
    ];
    
    const positions = projector.helper.geometry.attributes.position as THREE.BufferAttribute;
    const arr = positions.array as Float32Array;
    let idx = 0;
    
    // Near plane
    for (let i = 0; i < 4; i++) {
      const next = (i + 1) % 4;
      arr[idx++] = nearCorners[i].x; arr[idx++] = nearCorners[i].y; arr[idx++] = nearCorners[i].z;
      arr[idx++] = nearCorners[next].x; arr[idx++] = nearCorners[next].y; arr[idx++] = nearCorners[next].z;
    }
    
    // Far plane
    for (let i = 0; i < 4; i++) {
      const next = (i + 1) % 4;
      arr[idx++] = farCorners[i].x; arr[idx++] = farCorners[i].y; arr[idx++] = farCorners[i].z;
      arr[idx++] = farCorners[next].x; arr[idx++] = farCorners[next].y; arr[idx++] = farCorners[next].z;
    }
    
    // Connecting lines
    for (let i = 0; i < 4; i++) {
      arr[idx++] = nearCorners[i].x; arr[idx++] = nearCorners[i].y; arr[idx++] = nearCorners[i].z;
      arr[idx++] = farCorners[i].x; arr[idx++] = farCorners[i].y; arr[idx++] = farCorners[i].z;
    }
    
    positions.needsUpdate = true;
    projector.helper.matrix.copy(group.matrixWorld);
  }, []);

  // Add projector
  const addProjector = useCallback((modelId: string, withTestPattern?: boolean): Projector => {
    if (!sceneRef.current) throw new Error('Scene not initialized');
    
    const config = PROJECTOR_DATABASE[modelId];
    if (!config) throw new Error(`Unknown projector model: ${modelId}`);
    
    const id = ++projectorIdCounter.current;
    const defaultLens = LENSES[config.defaultLens];
    
    // Create group
    const group = new THREE.Group();
    const offset = projectors.length * 5;
    group.position.set(offset, 2.5, 10);
    sceneRef.current.add(group);
    
    // Create mesh
    const s = 0.0015;
    const geometry = new THREE.BoxGeometry(550 * s, 220 * s, 570 * s);
    const material = new THREE.MeshStandardMaterial({ color: 0x1a1a1a, metalness: 0.8, roughness: 0.2 });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.z = 570 * s / 2;
    mesh.userData = { type: 'projector', name: `${config.name} #${id}`, isProjector: true, projectorId: id };
    group.add(mesh);
    
    // Create lens visual
    const lensGeo = new THREE.CylinderGeometry(0.08, 0.10, 0.04, 32);
    const lensMat = new THREE.MeshBasicMaterial({ color: 0x00ffff });
    const lens = new THREE.Mesh(lensGeo, lensMat);
    lens.rotation.x = Math.PI / 2;
    lens.position.z = -570 * s / 2 - 0.02;
    mesh.add(lens);
    
    // Create projector camera
    const projCamera = new THREE.PerspectiveCamera(throwToFOV(defaultLens.throwMin), ASPECT, 0.1, PROJECTOR_CAMERA_FAR);
    group.add(projCamera);
    
    // Create spotlight for shadows
    const shadowLight = new THREE.SpotLight(0xffffff, 0.001);
    shadowLight.angle = THREE.MathUtils.degToRad(throwToFOV(defaultLens.throwMin) / 2);
    shadowLight.penumbra = 0;
    shadowLight.decay = 0;
    shadowLight.castShadow = true;
    shadowLight.shadow.mapSize.width = 2048;
    shadowLight.shadow.mapSize.height = 2048;
    group.add(shadowLight);
    
    // Create target mesh
    const targetGeo = new THREE.SphereGeometry(0.15, 32, 32);
    const targetMat = new THREE.MeshBasicMaterial({ color: 0xffff00 });
    const target = new THREE.Mesh(targetGeo, targetMat);
    target.position.set(group.position.x, group.position.y, group.position.z - 8);
    target.userData = { type: 'target', name: `Target #${id}`, isTarget: true, projectorId: id };
    sceneRef.current.add(target);
    
    // Create depth render target
    const depthRT = new THREE.WebGLRenderTarget(2048, 2048, {
      minFilter: THREE.NearestFilter,
      magFilter: THREE.NearestFilter,
      format: THREE.RGBAFormat,
      type: THREE.FloatType
    });
    
    // Create depth camera
    const depthCamera = new THREE.PerspectiveCamera(throwToFOV(defaultLens.throwMin), ASPECT, 0.1, 100);
    
    const projector: Projector = {
      id,
      config,
      group,
      camera: projCamera,
      mesh,
      target,
      helper: null as any,
      shadowLight,
      depthRenderTarget: depthRT,
      depthCamera,
      rtPreview: null,
      
      currentLensId: config.defaultLens,
      currentLens: defaultLens,
      throwRatio: defaultLens.throwMin,
      lensShiftV: 0,
      lensShiftH: 0,
      
      projDistance: 8,
      frustumFar: 100,
      projectionIntensity: 1.0,
      projectionTexture: null,
      orientation: 'landscape',
      
      keystoneV: 0,
      keystoneH: 0,
      keystoneTLX: 0,
      keystoneTLY: 0,
      keystoneTRX: 0,
      keystoneTRY: 0,
      keystoneBLX: 0,
      keystoneBLY: 0,
      keystoneBRX: 0,
      keystoneBRY: 0,
      
      softEdgeL: 0,
      softEdgeR: 0,
      softEdgeT: 0,
      softEdgeB: 0,
      softEdgeGamma: 2.2,
      
      targetLocked: false,
      userMovedTarget: false,
    };
    
    // Create and add helper
    const helper = createProjectorHelper(projector);
    sceneRef.current.add(helper);
    projector.helper = helper;
    updateProjectorHelper(projector);
    
    // Add test pattern if requested - inline creation
    if (withTestPattern && sceneRef.current) {
      const patternId = ++objectIdCounter.current;
      
      // Create test pattern texture
      const canvas = document.createElement('canvas');
      canvas.width = 1920;
      canvas.height = 1080;
      const ctx = canvas.getContext('2d')!;
      
      ctx.fillStyle = '#000000';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      for (let x = 0; x <= canvas.width; x += 120) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      }
      for (let y = 0; y <= canvas.height; y += 120) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }
      
      ctx.strokeStyle = '#ff0000';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(canvas.width / 2, 0);
      ctx.lineTo(canvas.width / 2, canvas.height);
      ctx.moveTo(0, canvas.height / 2);
      ctx.lineTo(canvas.width, canvas.height / 2);
      ctx.stroke();
      
      ctx.fillStyle = '#00ff00';
      const markerSize = 60;
      ctx.fillRect(0, 0, markerSize, markerSize);
      ctx.fillRect(canvas.width - markerSize, 0, markerSize, markerSize);
      ctx.fillRect(0, canvas.height - markerSize, markerSize, markerSize);
      ctx.fillRect(canvas.width - markerSize, canvas.height - markerSize, markerSize, markerSize);
      
      ctx.strokeStyle = '#00ffff';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.arc(canvas.width / 2, canvas.height / 2, 100, 0, Math.PI * 2);
      ctx.stroke();
      
      const texture = new THREE.CanvasTexture(canvas);
      texture.needsUpdate = true;
      
      const patternGeo = new THREE.PlaneGeometry(12, 12 * (9 / 16));
      const patternMat = new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide });
      const patternMesh = new THREE.Mesh(patternGeo, patternMat);
      
      patternMesh.position.set(group.position.x, group.position.y, group.position.z - projector.projDistance);
      patternMesh.userData = { type: 'screen', name: `Test Pattern ${patternId}`, objectId: patternId };
      
      sceneRef.current.add(patternMesh);
      
      const patternObj: SceneObject = {
        id: patternId,
        name: `Test Pattern ${patternId}`,
        type: 'screen',
        mesh: patternMesh,
        visible: true,
      };
      
      setObjects(prev => [...prev, patternObj]);
    }
    
    setProjectors(prev => [...prev, projector]);
    
    return projector;
  }, [projectors, createProjectorHelper, updateProjectorHelper]);

  // Add camera
  const addCamera = useCallback((): Camera3D => {
    if (!sceneRef.current) throw new Error('Scene not initialized');
    
    const id = ++cameraIdCounter.current;
    
    // Create group
    const group = new THREE.Group();
    group.position.set(10, 5, 10);
    sceneRef.current.add(group);
    
    // Create camera
    const cam = new THREE.PerspectiveCamera(50, 16 / 9, 0.1, 100);
    group.add(cam);
    
    // Create helper
    const helper = new THREE.CameraHelper(cam);
    sceneRef.current.add(helper);
    
    // Create mesh representation
    const geometry = new THREE.BoxGeometry(0.5, 0.3, 0.4);
    const material = new THREE.MeshStandardMaterial({ color: 0x3b82f6 });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.userData = { type: 'camera', name: `Camera #${id}`, isCamera: true, cameraId: id };
    group.add(mesh);
    
    // Create target
    const targetGeo = new THREE.SphereGeometry(0.1, 16, 16);
    const targetMat = new THREE.MeshBasicMaterial({ color: 0x60a5fa });
    const target = new THREE.Mesh(targetGeo, targetMat);
    target.position.set(0, 0, -5);
    group.add(target);
    
    const camera3D: Camera3D = {
      id,
      name: `Camera ${id}`,
      group,
      camera: cam,
      helper,
      target,
      mesh,
      fov: 50,
      near: 0.1,
      far: 100,
      aspect: 16 / 9,
      assignedToViewer: false,
      assignedToProjectorView: false,
      assignedToMappingPreview: false,
    };
    
    setCameras(prev => [...prev, camera3D]);
    
    return camera3D;
  }, []);

  // Add primitive
  const addPrimitive = useCallback((type: 'box' | 'plane' | 'sphere' | 'cylinder' | 'cone'): SceneObject => {
    if (!sceneRef.current) throw new Error('Scene not initialized');
    
    const id = ++objectIdCounter.current;
    let geometry: THREE.BufferGeometry;
    let name = '';
    
    switch (type) {
      case 'box':
        geometry = new THREE.BoxGeometry(2, 2, 2);
        name = `Box ${id}`;
        break;
      case 'plane':
        geometry = new THREE.PlaneGeometry(4, 4);
        name = `Plane ${id}`;
        break;
      case 'sphere':
        geometry = new THREE.SphereGeometry(1, 32, 32);
        name = `Sphere ${id}`;
        break;
      case 'cylinder':
        geometry = new THREE.CylinderGeometry(1, 1, 2, 32);
        name = `Cylinder ${id}`;
        break;
      case 'cone':
        geometry = new THREE.ConeGeometry(1, 2, 32);
        name = `Cone ${id}`;
        break;
    }
    
    const material = new THREE.MeshStandardMaterial({ 
      color: 0x888888,
      roughness: 0.7,
      metalness: 0.1
    });
    
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set((Math.random() - 0.5) * 6, 1 + Math.random() * 2, (Math.random() - 0.5) * 6);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    mesh.userData = { type: 'primitive', name, objectId: id };
    
    sceneRef.current.add(mesh);
    
    const sceneObject: SceneObject = {
      id,
      name,
      type: 'primitive',
      mesh,
      visible: true,
    };
    
    setObjects(prev => [...prev, sceneObject]);
    
    return sceneObject;
  }, []);

  // Add wall
  const addWall = useCallback((): SceneObject => {
    if (!sceneRef.current) throw new Error('Scene not initialized');
    
    const id = ++objectIdCounter.current;
    
    const geometry = new THREE.PlaneGeometry(12, 8);
    const material = new THREE.MeshStandardMaterial({ 
      color: 0xaaaaaa,
      side: THREE.DoubleSide,
      roughness: 0.8
    });
    
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(0, 4, -8);
    mesh.receiveShadow = true;
    mesh.userData = { type: 'wall', name: `Wall ${id}`, objectId: id };
    
    sceneRef.current.add(mesh);
    
    const sceneObject: SceneObject = {
      id,
      name: `Wall ${id}`,
      type: 'wall',
      mesh,
      visible: true,
    };
    
    setObjects(prev => [...prev, sceneObject]);
    
    return sceneObject;
  }, []);

  // Add test pattern (mire)
  const addTestPattern = useCallback((projector: Projector): SceneObject => {
    if (!sceneRef.current) throw new Error('Scene not initialized');
    
    const id = ++objectIdCounter.current;
    
    // Create test pattern texture
    const canvas = document.createElement('canvas');
    canvas.width = 1920;
    canvas.height = 1080;
    const ctx = canvas.getContext('2d')!;
    
    // Background
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    
    // Vertical lines
    for (let x = 0; x <= canvas.width; x += 120) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }
    
    // Horizontal lines
    for (let y = 0; y <= canvas.height; y += 120) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvas.width, y);
      ctx.stroke();
    }
    
    // Center cross
    ctx.strokeStyle = '#ff0000';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.moveTo(0, canvas.height / 2);
    ctx.lineTo(canvas.width, canvas.height / 2);
    ctx.stroke();
    
    // Corner markers
    ctx.fillStyle = '#00ff00';
    const markerSize = 60;
    ctx.fillRect(0, 0, markerSize, markerSize);
    ctx.fillRect(canvas.width - markerSize, 0, markerSize, markerSize);
    ctx.fillRect(0, canvas.height - markerSize, markerSize, markerSize);
    ctx.fillRect(canvas.width - markerSize, canvas.height - markerSize, markerSize, markerSize);
    
    // Center circle
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, 100, 0, Math.PI * 2);
    ctx.stroke();
    
    // Create texture from canvas
    const texture = new THREE.CanvasTexture(canvas);
    texture.needsUpdate = true;
    
    const geometry = new THREE.PlaneGeometry(12, 12 * (9 / 16));
    const material = new THREE.MeshBasicMaterial({ 
      map: texture,
      side: THREE.DoubleSide
    });
    
    const mesh = new THREE.Mesh(geometry, material);
    
    // Position in front of projector
    const projPos = projector.group.position;
    mesh.position.set(projPos.x, projPos.y, projPos.z - projector.projDistance);
    mesh.userData = { type: 'screen', name: `Test Pattern ${id}`, objectId: id };
    
    sceneRef.current.add(mesh);
    
    const sceneObject: SceneObject = {
      id,
      name: `Test Pattern ${id}`,
      type: 'screen',
      mesh,
      visible: true,
    };
    
    setObjects(prev => [...prev, sceneObject]);
    
    return sceneObject;
  }, []);

  // Select object
  const selectObject = useCallback((obj: THREE.Object3D | null) => {
    if (!transformControlsRef.current) return;
    
    if (obj) {
      transformControlsRef.current.attach(obj);
      
      // Determine type and instance
      const userData = obj.userData || {};
      if (userData.isProjector) {
        const proj = projectors.find(p => p.id === userData.projectorId);
        setSelection({ type: 'projector', object: obj, instance: proj || null });
      } else if (userData.isCamera) {
        const cam = cameras.find(c => c.id === userData.cameraId);
        setSelection({ type: 'camera', object: obj, instance: cam || null });
      } else if (userData.isTarget) {
        const proj = projectors.find(p => p.id === userData.projectorId);
        setSelection({ type: 'target', object: obj, instance: proj || null });
      } else {
        const sceneObj = objects.find(o => o.id === userData.objectId);
        setSelection({ type: 'object', object: obj, instance: sceneObj || null });
      }
    } else {
      transformControlsRef.current.detach();
      setSelection({ type: null, object: null, instance: null });
    }
  }, [projectors, cameras, objects]);

  // Set transform mode
  const setTransformMode = useCallback((mode: TransformMode) => {
    if (transformControlsRef.current) {
      transformControlsRef.current.setMode(mode);
    }
    setTransformModeState(mode);
  }, []);

  // Load content
  const loadContent = useCallback(async (file: File): Promise<void> => {
    const url = URL.createObjectURL(file);
    
    if (file.type.startsWith('video/')) {
      const video = document.createElement('video');
      video.src = url;
      video.crossOrigin = 'anonymous';
      video.loop = true;
      video.muted = true;
      video.playsInline = true;
      
      await video.play().catch(() => {});
      
      const videoTex = new THREE.VideoTexture(video);
      videoTex.minFilter = THREE.LinearFilter;
      videoTex.magFilter = THREE.LinearFilter;
      videoTex.format = THREE.RGBAFormat;
      videoTex.generateMipmaps = false;
      
      setContentVideo(video);
      setContentTexture(videoTex);
    } else if (file.type.startsWith('image/')) {
      const loader = new THREE.TextureLoader();
      const texture = await loader.loadAsync(url);
      texture.minFilter = THREE.LinearFilter;
      texture.magFilter = THREE.LinearFilter;
      
      setContentTexture(texture);
    }
  }, []);

  // Set camera view
  const setCameraView = useCallback((view: 'top' | 'front' | 'left' | 'right' | 'back' | 'perspective') => {
    if (!cameraRef.current || !orbitControlsRef.current) return;
    
    const camera = cameraRef.current;
    const controls = orbitControlsRef.current;
    const distance = 20;
    const target = new THREE.Vector3(0, 0, 0);
    
    switch (view) {
      case 'top':
        camera.position.set(0, distance, 0);
        camera.up.set(0, 0, -1);
        break;
      case 'front':
        camera.position.set(0, 0, distance);
        camera.up.set(0, 1, 0);
        break;
      case 'left':
        camera.position.set(-distance, 0, 0);
        camera.up.set(0, 1, 0);
        break;
      case 'right':
        camera.position.set(distance, 0, 0);
        camera.up.set(0, 1, 0);
        break;
      case 'back':
        camera.position.set(0, 0, -distance);
        camera.up.set(0, 1, 0);
        break;
      case 'perspective':
      default:
        camera.position.set(15, 10, 15);
        camera.up.set(0, 1, 0);
        break;
    }
    
    camera.lookAt(target);
    controls.target.copy(target);
    controls.update();
  }, []);

  // Delete selected
  const deleteSelected = useCallback(() => {
    if (!selection.object || !sceneRef.current) return;
    
    const userData = selection.object.userData || {};
    
    if (userData.isProjector) {
      const proj = projectors.find(p => p.id === userData.projectorId);
      if (proj) {
        sceneRef.current.remove(proj.group);
        sceneRef.current.remove(proj.helper);
        sceneRef.current.remove(proj.target);
        setProjectors(prev => prev.filter(p => p.id !== proj.id));
      }
    } else if (userData.isCamera) {
      const cam = cameras.find(c => c.id === userData.cameraId);
      if (cam) {
        sceneRef.current.remove(cam.group);
        sceneRef.current.remove(cam.helper);
        setCameras(prev => prev.filter(c => c.id !== cam.id));
      }
    } else if (userData.objectId) {
      const obj = objects.find(o => o.id === userData.objectId);
      if (obj) {
        sceneRef.current.remove(obj.mesh);
        setObjects(prev => prev.filter(o => o.id !== obj.id));
      }
    }
    
    transformControlsRef.current?.detach();
    setSelection({ type: null, object: null, instance: null });
  }, [selection, projectors, cameras, objects]);

  // Update projector settings
  const updateProjectorSettings = useCallback((projectorId: number, settings: Partial<Projector>) => {
    setProjectors(prev => prev.map(p => {
      if (p.id !== projectorId) return p;
      
      const updated = { ...p, ...settings };
      
      // Update camera FOV if throw ratio changed
      if (settings.throwRatio !== undefined) {
        const fov = throwToFOV(settings.throwRatio);
        updated.camera.fov = fov;
        updated.camera.updateProjectionMatrix();
      }
      
      // Update aspect if orientation changed
      if (settings.orientation !== undefined) {
        const aspect = settings.orientation === 'portrait' ? 9 / 16 : 16 / 9;
        updated.camera.aspect = aspect;
        updated.camera.updateProjectionMatrix();
      }
      
      updateProjectorHelper(updated);
      
      return updated;
    }));
  }, [updateProjectorHelper]);

  // Render to canvas
  const renderToCanvas = useCallback((canvas: HTMLCanvasElement, cam: THREE.Camera, width: number, height: number) => {
    if (!rendererRef.current || !sceneRef.current) return;
    
    const renderer = rendererRef.current;
    const scene = sceneRef.current;
    
    const rt = new THREE.WebGLRenderTarget(width, height, {
      minFilter: THREE.LinearFilter,
      magFilter: THREE.LinearFilter,
      format: THREE.RGBAFormat,
    });
    
    renderer.setRenderTarget(rt);
    renderer.clear();
    renderer.render(scene, cam);
    renderer.setRenderTarget(null);
    
    const pixels = new Uint8Array(width * height * 4);
    renderer.readRenderTargetPixels(rt, 0, 0, width, height, pixels);
    rt.dispose();
    
    // Flip vertically
    const out = new Uint8ClampedArray(width * height * 4);
    for (let y = 0; y < height; y++) {
      const src = y * width * 4;
      const dst = (height - 1 - y) * width * 4;
      out.set(pixels.subarray(src, src + width * 4), dst);
    }
    
    const ctx = canvas.getContext('2d');
    if (ctx) {
      const imageData = new ImageData(out, width, height);
      ctx.putImageData(imageData, 0, 0);
    }
  }, []);

  // Get active projector
  const getActiveProjector = useCallback((): Projector | null => {
    if (selection.type === 'projector' && selection.instance) {
      return selection.instance as Projector;
    }
    return projectors[0] || null;
  }, [selection, projectors]);

  // Toggle grid
  const toggleGrid = useCallback(() => {
    if (gridHelperRef.current && axesHelperRef.current) {
      const newVisible = !gridHelperRef.current.visible;
      gridHelperRef.current.visible = newVisible;
      axesHelperRef.current.visible = newVisible;
      setGridVisible(newVisible);
    }
  }, []);

  // Set projector orientation
  const setProjectorOrientation = useCallback((projectorId: number, orientation: 'portrait' | 'landscape') => {
    updateProjectorSettings(projectorId, { orientation });
  }, [updateProjectorSettings]);

  // Update camera settings
  const updateCameraSettings = useCallback((cameraId: number, settings: Partial<Camera3D>) => {
    setCameras(prev => prev.map(c => {
      if (c.id !== cameraId) return c;
      
      const updated = { ...c, ...settings };
      
      // Update actual camera properties
      if (settings.fov !== undefined) {
        updated.camera.fov = settings.fov;
        updated.camera.updateProjectionMatrix();
        updated.helper.update();
      }
      if (settings.near !== undefined) {
        updated.camera.near = settings.near;
        updated.camera.updateProjectionMatrix();
        updated.helper.update();
      }
      if (settings.far !== undefined) {
        updated.camera.far = settings.far;
        updated.camera.updateProjectionMatrix();
        updated.helper.update();
      }
      if (settings.aspect !== undefined) {
        updated.camera.aspect = settings.aspect;
        updated.camera.updateProjectionMatrix();
        updated.helper.update();
      }
      
      return updated;
    }));
  }, []);

  // Assign camera to projector view
  const assignCameraToProjectorView = useCallback((cameraId: number, assigned: boolean) => {
    setCameras(prev => prev.map(c => ({
      ...c,
      assignedToProjectorView: c.id === cameraId ? assigned : (assigned ? false : c.assignedToProjectorView)
    })));
    
    if (assigned) {
      const cam = cameras.find(c => c.id === cameraId);
      setProjectorViewCamera(cam || null);
    } else {
      setProjectorViewCamera(null);
    }
  }, [cameras]);

  // Assign camera to mapping preview
  const assignCameraToMappingPreview = useCallback((cameraId: number, assigned: boolean) => {
    setCameras(prev => prev.map(c => ({
      ...c,
      assignedToMappingPreview: c.id === cameraId ? assigned : (assigned ? false : c.assignedToMappingPreview)
    })));
    
    if (assigned) {
      const cam = cameras.find(c => c.id === cameraId);
      setMappingPreviewCamera(cam || null);
    } else {
      setMappingPreviewCamera(null);
    }
  }, [cameras]);

  return {
    scene: sceneRef.current,
    camera: cameraRef.current,
    renderer: rendererRef.current,
    projectors,
    cameras,
    objects,
    selection,
    transformMode,
    contentTexture,
    contentVideo,
    timeline,
    recording,
    projectorViewCamera,
    mappingPreviewCamera,
    
    addProjector,
    addCamera,
    addPrimitive,
    addWall,
    addTestPattern,
    selectObject,
    setTransformMode,
    loadContent,
    setCameraView,
    deleteSelected,
    updateProjectorSettings,
    updateCameraSettings,
    assignCameraToProjectorView,
    assignCameraToMappingPreview,
    renderToCanvas,
    getActiveProjector,
    toggleGrid,
    setProjectorOrientation,
  };
};
