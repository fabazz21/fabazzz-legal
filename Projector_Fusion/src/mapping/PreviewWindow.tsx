import React, { useRef, useEffect } from 'react';
import { Download, Maximize2 } from 'lucide-react';
import * as THREE from 'three';

interface PreviewWindowProps {
  title: string;
  type: 'projector' | 'main';
  camera: THREE.Camera | null;
  scene: THREE.Scene | null;
  renderer: THREE.WebGLRenderer | null;
  width?: number;
  height?: number;
  onDownload?: () => void;
}

export const PreviewWindow: React.FC<PreviewWindowProps> = ({
  title,
  type,
  camera,
  scene,
  renderer,
  width = 400,
  height = 225,
  onDownload,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameRef = useRef<number>();

  useEffect(() => {
    if (!canvasRef.current || !camera || !scene || !renderer) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const w = Math.floor(width * dpr);
    const h = Math.floor(height * dpr);

    canvas.width = w;
    canvas.height = h;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;

    const renderTarget = new THREE.WebGLRenderTarget(w, h, {
      minFilter: THREE.LinearFilter,
      magFilter: THREE.LinearFilter,
      format: THREE.RGBAFormat,
    });

    const renderPreview = () => {
      renderer.setRenderTarget(renderTarget);
      renderer.clear();
      renderer.render(scene, camera);
      renderer.setRenderTarget(null);

      const pixels = new Uint8Array(w * h * 4);
      renderer.readRenderTargetPixels(renderTarget, 0, 0, w, h, pixels);

      // Flip vertically
      const out = new Uint8ClampedArray(w * h * 4);
      for (let y = 0; y < h; y++) {
        const src = y * w * 4;
        const dst = (h - 1 - y) * w * 4;
        out.set(pixels.subarray(src, src + w * 4), dst);
      }

      const imageData = new ImageData(out, w, h);
      ctx.putImageData(imageData, 0, 0);

      animationFrameRef.current = requestAnimationFrame(renderPreview);
    };

    renderPreview();

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      renderTarget.dispose();
    };
  }, [camera, scene, renderer, width, height]);

  return (
    <div className="preview-window">
      <div className={type === 'projector' ? 'preview-label' : 'preview-label-secondary'}>
        <span className="flex items-center gap-2">
          {type === 'projector' ? '📽️' : '🎥'}
          {title}
        </span>
      </div>
      
      <canvas 
        ref={canvasRef}
        className="w-full h-auto bg-black"
      />
      
      <div className="absolute bottom-2 right-2 flex gap-1">
        <button 
          className="p-1.5 bg-black/50 hover:bg-black/70 rounded text-white/70 hover:text-white transition-colors"
          onClick={onDownload}
          title="Download"
        >
          <Download className="w-3 h-3" />
        </button>
        <button 
          className="p-1.5 bg-black/50 hover:bg-black/70 rounded text-white/70 hover:text-white transition-colors"
          title="Fullscreen"
        >
          <Maximize2 className="w-3 h-3" />
        </button>
      </div>
    </div>
  );
};
