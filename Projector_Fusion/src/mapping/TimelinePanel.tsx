import React, { useState } from 'react';
import { Play, Pause, SkipBack, SkipForward, Plus, ChevronDown, Lock, Eye, EyeOff } from 'lucide-react';
import { Timeline, TimelineLayer } from '@/types/mapping';

interface TimelinePanelProps {
  timeline: Timeline;
  onPlayPause: () => void;
  onSeek: (time: number) => void;
  onAddKeyframe: () => void;
  onToggleLayerVisibility: (layerId: number) => void;
  onToggleLayerLock: (layerId: number) => void;
  visible: boolean;
  onToggleVisibility: () => void;
}

export const TimelinePanel: React.FC<TimelinePanelProps> = ({
  timeline,
  onPlayPause,
  onSeek,
  onAddKeyframe,
  onToggleLayerVisibility,
  onToggleLayerLock,
  visible,
  onToggleVisibility,
}) => {
  const [zoom, setZoom] = useState(1);
  
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    const frames = Math.floor((seconds % 1) * timeline.fps);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}:${frames.toString().padStart(2, '0')}`;
  };

  const playheadPosition = (timeline.currentTime / timeline.duration) * 100;

  if (!visible) {
    return (
      <button 
        className="fixed bottom-4 left-1/2 -translate-x-1/2 menu-btn flex items-center gap-2"
        onClick={onToggleVisibility}
      >
        <ChevronDown className="w-4 h-4 rotate-180" />
        Show Timeline
      </button>
    );
  }

  return (
    <div className="timeline-container h-48 flex flex-col">
      {/* Timeline Header */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-border bg-panel-header">
        <div className="flex items-center gap-4">
          {/* Transport Controls */}
          <div className="flex items-center gap-1">
            <button 
              className="gizmo-btn"
              onClick={() => onSeek(0)}
              title="Go to Start"
            >
              <SkipBack className="w-3 h-3" />
            </button>
            <button 
              className={`gizmo-btn ${timeline.playing ? 'active' : ''}`}
              onClick={onPlayPause}
              title={timeline.playing ? 'Pause' : 'Play'}
            >
              {timeline.playing ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            </button>
            <button 
              className="gizmo-btn"
              onClick={() => onSeek(timeline.duration)}
              title="Go to End"
            >
              <SkipForward className="w-3 h-3" />
            </button>
          </div>

          {/* Time Display */}
          <div className="font-mono text-xs text-primary bg-muted px-3 py-1 rounded">
            {formatTime(timeline.currentTime)} / {formatTime(timeline.duration)}
          </div>

          {/* Add Keyframe */}
          <button 
            className="menu-btn flex items-center gap-1"
            onClick={onAddKeyframe}
          >
            <Plus className="w-3 h-3" />
            Key (K)
          </button>
        </div>

        <div className="flex items-center gap-4">
          {/* FPS Display */}
          <div className="text-xs text-muted-foreground">
            {timeline.fps} FPS
          </div>

          {/* Zoom */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-muted-foreground">Zoom:</span>
            <input 
              type="range"
              className="control-slider w-20"
              min={0.5}
              max={4}
              step={0.1}
              value={zoom}
              onChange={(e) => setZoom(parseFloat(e.target.value))}
            />
          </div>

          <button 
            className="gizmo-btn"
            onClick={onToggleVisibility}
            title="Hide Timeline"
          >
            <ChevronDown className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Timeline Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Layers List */}
        <div className="w-48 border-r border-border overflow-y-auto bg-muted/20">
          {timeline.layers.length === 0 ? (
            <div className="p-4 text-center text-muted-foreground text-xs">
              <p>No layers</p>
              <p className="mt-1">Select an object and press K to add keyframes</p>
            </div>
          ) : (
            timeline.layers.map(layer => (
              <div 
                key={layer.id}
                className="flex items-center gap-2 px-2 py-1.5 border-b border-border/50 hover:bg-accent/30"
              >
                <div 
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: layer.color }}
                />
                <span className="flex-1 text-xs truncate">{layer.name}</span>
                <button 
                  className="p-1 hover:bg-accent rounded"
                  onClick={() => onToggleLayerVisibility(layer.id)}
                >
                  {layer.visible ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
                </button>
                <button 
                  className={`p-1 hover:bg-accent rounded ${layer.locked ? 'text-warning' : ''}`}
                  onClick={() => onToggleLayerLock(layer.id)}
                >
                  <Lock className="w-3 h-3" />
                </button>
              </div>
            ))
          )}
        </div>

        {/* Timeline Tracks */}
        <div className="flex-1 relative overflow-x-auto">
          {/* Time Ruler */}
          <div className="h-6 border-b border-border bg-muted/30 flex items-end">
            {Array.from({ length: Math.ceil(timeline.duration) + 1 }).map((_, i) => (
              <div 
                key={i}
                className="flex-shrink-0 text-[10px] text-muted-foreground border-l border-border/50 pl-1"
                style={{ width: `${100 / timeline.duration * zoom}%` }}
              >
                {i}s
              </div>
            ))}
          </div>

          {/* Tracks */}
          <div className="relative">
            {timeline.layers.map(layer => (
              <div 
                key={layer.id}
                className="h-8 border-b border-border/30 relative"
              >
                {layer.keyframes.map((kf, i) => (
                  <div 
                    key={i}
                    className="keyframe-marker"
                    style={{ 
                      left: `${(kf.time / timeline.duration) * 100 * zoom}%`,
                      backgroundColor: layer.color,
                    }}
                    title={`${kf.property} @ ${kf.time.toFixed(2)}s`}
                  />
                ))}
              </div>
            ))}

            {/* Playhead */}
            <div 
              className="timeline-playhead z-10"
              style={{ left: `${playheadPosition * zoom}%` }}
            >
              <div className="absolute -top-6 left-1/2 -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-destructive" />
            </div>
          </div>

          {/* Click to seek overlay */}
          <div 
            className="absolute top-6 left-0 right-0 bottom-0 cursor-pointer"
            onClick={(e) => {
              const rect = e.currentTarget.getBoundingClientRect();
              const x = e.clientX - rect.left;
              const time = (x / rect.width / zoom) * timeline.duration;
              onSeek(Math.max(0, Math.min(timeline.duration, time)));
            }}
          />
        </div>
      </div>
    </div>
  );
};
