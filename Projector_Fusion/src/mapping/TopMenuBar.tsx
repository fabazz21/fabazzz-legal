import React from 'react';
import { 
  Projector, 
  Move, 
  RotateCcw, 
  Maximize2, 
  Grid3X3, 
  Camera, 
  Save, 
  FolderOpen,
  Play,
  Square,
  Circle,
  Download,
  Trash2,
  Eye
} from 'lucide-react';
import { TransformMode } from '@/types/mapping';

interface TopMenuBarProps {
  onAddProjector: () => void;
  onAddCamera: () => void;
  onAddPrimitive: (type: 'box' | 'plane' | 'sphere' | 'cylinder' | 'cone') => void;
  onAddWall: () => void;
  onLoadContent: () => void;
  onExport: () => void;
  onToggleRecording: () => void;
  onPlay: () => void;
  onPause: () => void;
  onSetTransformMode: (mode: TransformMode) => void;
  onToggleGrid: () => void;
  onSetCameraView: (view: 'top' | 'front' | 'left' | 'right' | 'back' | 'perspective') => void;
  onDelete: () => void;
  transformMode: TransformMode;
  isRecording: boolean;
  isPlaying: boolean;
  hasSelection: boolean;
}

export const TopMenuBar: React.FC<TopMenuBarProps> = ({
  onAddProjector,
  onAddCamera,
  onAddPrimitive,
  onAddWall,
  onLoadContent,
  onExport,
  onToggleRecording,
  onPlay,
  onPause,
  onSetTransformMode,
  onToggleGrid,
  onSetCameraView,
  onDelete,
  transformMode,
  isRecording,
  isPlaying,
  hasSelection,
}) => {
  return (
    <div className="top-menu-bar">
      {/* Logo */}
      <div className="flex items-center gap-2 pr-4 border-r border-border">
        <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
          <Projector className="w-4 h-4 text-primary" />
        </div>
        <span className="font-bold text-primary">3D Mapping Pro</span>
      </div>

      {/* Navigation Tabs */}
      <div className="nav-tabs ml-4">
        <button className="nav-tab active">Setup</button>
        <button className="nav-tab">Calibration</button>
        <button className="nav-tab">Export</button>
      </div>

      {/* Camera Views Dropdown */}
      <select 
        className="control-select w-32 ml-4"
        onChange={(e) => onSetCameraView(e.target.value as any)}
        defaultValue=""
      >
        <option value="" disabled>🎥 Views</option>
        <option value="top">⬆️ Top</option>
        <option value="front">➡️ Front</option>
        <option value="left">⬅️ Left</option>
        <option value="right">➡️ Right</option>
        <option value="back">⬅️ Back</option>
        <option value="perspective">🎥 Perspective</option>
      </select>

      {/* Transform Gizmo Controls */}
      <div className="flex gap-1 ml-4">
        <button 
          className={`gizmo-btn ${transformMode === 'translate' ? 'active' : ''}`}
          onClick={() => onSetTransformMode('translate')}
          title="Move (G)"
        >
          <Move className="w-4 h-4" />
        </button>
        <button 
          className={`gizmo-btn ${transformMode === 'rotate' ? 'active' : ''}`}
          onClick={() => onSetTransformMode('rotate')}
          title="Rotate (R)"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
        <button 
          className={`gizmo-btn ${transformMode === 'scale' ? 'active' : ''}`}
          onClick={() => onSetTransformMode('scale')}
          title="Scale (S)"
        >
          <Maximize2 className="w-4 h-4" />
        </button>
      </div>

      {/* Grid Toggle */}
      <button 
        className="menu-btn ml-4"
        onClick={onToggleGrid}
        title="Toggle Grid"
      >
        <Grid3X3 className="w-3 h-3 inline mr-1" />
        Grid
      </button>

      {/* Playback Controls */}
      <div className="flex gap-2 ml-4 pl-4 border-l border-border">
        <button 
          className="menu-btn"
          onClick={isPlaying ? onPause : onPlay}
        >
          {isPlaying ? (
            <Square className="w-3 h-3 inline mr-1" />
          ) : (
            <Play className="w-3 h-3 inline mr-1" />
          )}
          {isPlaying ? 'Pause' : 'Play'}
        </button>
        <button 
          className={`menu-btn-danger flex items-center gap-1 ${isRecording ? 'animate-pulse' : ''}`}
          onClick={onToggleRecording}
        >
          {isRecording && <span className="recording-indicator" />}
          <Circle className="w-3 h-3" />
          {isRecording ? 'Stop' : 'Record'}
        </button>
      </div>

      {/* Export */}
      <button 
        className="menu-btn ml-2"
        onClick={onExport}
      >
        <Download className="w-3 h-3 inline mr-1" />
        Export
      </button>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Action Buttons */}
      <div className="flex gap-2">
        {/* Add Primitives Dropdown */}
        <div className="relative group">
          <button className="menu-btn">
            🔷 Add
          </button>
          <div className="absolute right-0 top-full mt-1 hidden group-hover:block z-50">
            <div className="bg-popover border border-border rounded-lg shadow-xl p-2 min-w-[160px]">
              <button 
                className="w-full text-left px-3 py-2 text-xs rounded hover:bg-accent"
                onClick={() => onAddPrimitive('box')}
              >
                ⬛ Cube
              </button>
              <button 
                className="w-full text-left px-3 py-2 text-xs rounded hover:bg-accent"
                onClick={() => onAddPrimitive('sphere')}
              >
                ⚫ Sphere
              </button>
              <button 
                className="w-full text-left px-3 py-2 text-xs rounded hover:bg-accent"
                onClick={() => onAddPrimitive('plane')}
              >
                ▭ Plane
              </button>
              <button 
                className="w-full text-left px-3 py-2 text-xs rounded hover:bg-accent"
                onClick={() => onAddPrimitive('cylinder')}
              >
                ⬜ Cylinder
              </button>
              <button 
                className="w-full text-left px-3 py-2 text-xs rounded hover:bg-accent"
                onClick={() => onAddPrimitive('cone')}
              >
                🔺 Cone
              </button>
              <div className="border-t border-border my-1" />
              <button 
                className="w-full text-left px-3 py-2 text-xs rounded hover:bg-accent"
                onClick={onAddWall}
              >
                🧱 Wall / Screen
              </button>
            </div>
          </div>
        </div>

        <button className="menu-btn" onClick={onLoadContent}>
          <FolderOpen className="w-3 h-3 inline mr-1" />
          Content
        </button>

        <button className="menu-btn" onClick={onAddCamera}>
          <Camera className="w-3 h-3 inline mr-1" />
          Camera
        </button>

        <button 
          className="menu-btn-primary"
          onClick={onAddProjector}
        >
          <Projector className="w-3 h-3 inline mr-1" />
          + Projector
        </button>

        {hasSelection && (
          <button 
            className="menu-btn-danger"
            onClick={onDelete}
          >
            <Trash2 className="w-3 h-3" />
          </button>
        )}
      </div>
    </div>
  );
};
