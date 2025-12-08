import React from 'react';
import { ChevronDown, Camera, Eye, Video, Target, Settings } from 'lucide-react';
import { Camera3D } from '@/types/mapping';

interface CameraPropertiesPanelProps {
  camera: Camera3D;
  onUpdateCamera: (cameraId: number, settings: Partial<Camera3D>) => void;
  onAssignToProjectorView: (cameraId: number, assigned: boolean) => void;
  onAssignToMappingPreview: (cameraId: number, assigned: boolean) => void;
  assignedToProjectorView: boolean;
  assignedToMappingPreview: boolean;
}

export const CameraPropertiesPanel: React.FC<CameraPropertiesPanelProps> = ({
  camera,
  onUpdateCamera,
  onAssignToProjectorView,
  onAssignToMappingPreview,
  assignedToProjectorView,
  assignedToMappingPreview,
}) => {
  const [settingsExpanded, setSettingsExpanded] = React.useState(true);
  const [assignmentExpanded, setAssignmentExpanded] = React.useState(true);
  const [transformExpanded, setTransformExpanded] = React.useState(true);

  return (
    <div className="w-80 h-full overflow-y-auto bg-sidebar border-l border-border">
      {/* Camera Info Header */}
      <div className="p-4 border-b border-border bg-gradient-to-r from-blue-500/10 to-transparent">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center">
            <Camera className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <div className="font-semibold text-sm">{camera.name}</div>
            <div className="text-xs text-muted-foreground">FOV: {camera.fov}° • AR: {camera.aspect.toFixed(2)}</div>
          </div>
        </div>
      </div>

      {/* Assignment Section - IMPORTANT */}
      <div className="control-panel m-2 border-2 border-blue-500/30">
        <div 
          className="collapsible-header"
          onClick={() => setAssignmentExpanded(!assignmentExpanded)}
        >
          <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 uppercase">
            <Video className="w-4 h-4" />
            <span>Assignation Caméra</span>
          </div>
          <ChevronDown className={`chevron w-4 h-4 text-muted-foreground ${assignmentExpanded ? 'open' : ''}`} />
        </div>
        
        {assignmentExpanded && (
          <div className="panel-content space-y-3">
            {/* Assign to Projector View */}
            <label className="flex items-center gap-3 p-3 bg-primary/10 rounded-lg cursor-pointer hover:bg-primary/20 transition-all">
              <input 
                type="checkbox"
                checked={assignedToProjectorView}
                onChange={(e) => onAssignToProjectorView(camera.id, e.target.checked)}
                className="w-5 h-5 accent-primary rounded"
              />
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-lg">📽️</span>
                  <span className="text-sm font-medium">Projector Output</span>
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Utiliser cette caméra pour la vue projecteur
                </p>
              </div>
            </label>

            {/* Assign to Mapping Preview */}
            <label className="flex items-center gap-3 p-3 bg-accent/10 rounded-lg cursor-pointer hover:bg-accent/20 transition-all">
              <input 
                type="checkbox"
                checked={assignedToMappingPreview}
                onChange={(e) => onAssignToMappingPreview(camera.id, e.target.checked)}
                className="w-5 h-5 accent-accent rounded"
              />
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-lg">🎥</span>
                  <span className="text-sm font-medium">Mapping Preview</span>
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Utiliser cette caméra pour la preview mapping
                </p>
              </div>
            </label>

            {(assignedToProjectorView || assignedToMappingPreview) && (
              <div className="p-2 bg-green-500/10 border border-green-500/30 rounded text-xs text-green-400 text-center">
                ✓ Caméra assignée {assignedToProjectorView && assignedToMappingPreview ? 'aux deux vues' : 
                  assignedToProjectorView ? 'au Projector Output' : 'au Mapping Preview'}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Camera Settings */}
      <div className="control-panel m-2">
        <div 
          className="collapsible-header"
          onClick={() => setSettingsExpanded(!settingsExpanded)}
        >
          <div className="flex items-center gap-2 text-xs font-semibold text-primary uppercase">
            <Settings className="w-4 h-4" />
            <span>Paramètres Caméra</span>
          </div>
          <ChevronDown className={`chevron w-4 h-4 text-muted-foreground ${settingsExpanded ? 'open' : ''}`} />
        </div>
        
        {settingsExpanded && (
          <div className="panel-content space-y-4">
            {/* FOV */}
            <div>
              <label className="text-xs text-muted-foreground flex justify-between mb-2">
                <span>Champ de vision (FOV)</span>
                <span className="text-primary font-semibold">{camera.fov}°</span>
              </label>
              <input 
                type="range"
                className="control-slider"
                min={10}
                max={120}
                value={camera.fov}
                onChange={(e) => onUpdateCamera(camera.id, { fov: parseInt(e.target.value) })}
              />
            </div>

            {/* Near Clip */}
            <div>
              <label className="text-xs text-muted-foreground flex justify-between mb-2">
                <span>Near Clip</span>
                <span className="text-primary font-semibold">{camera.near.toFixed(2)}</span>
              </label>
              <input 
                type="range"
                className="control-slider"
                min={0.01}
                max={10}
                step={0.01}
                value={camera.near}
                onChange={(e) => onUpdateCamera(camera.id, { near: parseFloat(e.target.value) })}
              />
            </div>

            {/* Far Clip */}
            <div>
              <label className="text-xs text-muted-foreground flex justify-between mb-2">
                <span>Far Clip</span>
                <span className="text-primary font-semibold">{camera.far.toFixed(0)}</span>
              </label>
              <input 
                type="range"
                className="control-slider"
                min={10}
                max={1000}
                step={10}
                value={camera.far}
                onChange={(e) => onUpdateCamera(camera.id, { far: parseFloat(e.target.value) })}
              />
            </div>

            {/* Aspect Ratio */}
            <div>
              <label className="text-xs text-muted-foreground block mb-2">Aspect Ratio</label>
              <div className="flex gap-2">
                <button 
                  className={`flex-1 py-2 text-xs rounded ${camera.aspect === 16/9 ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}
                  onClick={() => onUpdateCamera(camera.id, { aspect: 16/9 })}
                >
                  16:9
                </button>
                <button 
                  className={`flex-1 py-2 text-xs rounded ${camera.aspect === 4/3 ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}
                  onClick={() => onUpdateCamera(camera.id, { aspect: 4/3 })}
                >
                  4:3
                </button>
                <button 
                  className={`flex-1 py-2 text-xs rounded ${camera.aspect === 1 ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}
                  onClick={() => onUpdateCamera(camera.id, { aspect: 1 })}
                >
                  1:1
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Transform Display */}
      <div className="control-panel m-2">
        <div 
          className="collapsible-header"
          onClick={() => setTransformExpanded(!transformExpanded)}
        >
          <div className="flex items-center gap-2 text-xs font-semibold text-primary uppercase">
            <Target className="w-4 h-4" />
            <span>Transform</span>
          </div>
          <ChevronDown className={`chevron w-4 h-4 text-muted-foreground ${transformExpanded ? 'open' : ''}`} />
        </div>
        
        {transformExpanded && (
          <div className="panel-content">
            <div className="grid grid-cols-3 gap-2">
              <div>
                <label className="text-[10px] text-muted-foreground block mb-1 text-center">X</label>
                <input 
                  type="number"
                  className="control-input text-center text-xs"
                  value={camera.group.position.x.toFixed(2)}
                  readOnly
                />
              </div>
              <div>
                <label className="text-[10px] text-muted-foreground block mb-1 text-center">Y</label>
                <input 
                  type="number"
                  className="control-input text-center text-xs"
                  value={camera.group.position.y.toFixed(2)}
                  readOnly
                />
              </div>
              <div>
                <label className="text-[10px] text-muted-foreground block mb-1 text-center">Z</label>
                <input 
                  type="number"
                  className="control-input text-center text-xs"
                  value={camera.group.position.z.toFixed(2)}
                  readOnly
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
