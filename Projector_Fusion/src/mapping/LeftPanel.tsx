import React, { useState } from 'react';
import { ChevronDown, Eye, EyeOff, Projector, Camera, Box, Trash2 } from 'lucide-react';
import { Projector as ProjectorType, Camera3D, SceneObject, Selection } from '@/types/mapping';

interface LeftPanelProps {
  projectors: ProjectorType[];
  cameras: Camera3D[];
  objects: SceneObject[];
  selection: Selection;
  onSelectProjector: (projector: ProjectorType) => void;
  onSelectCamera: (camera: Camera3D) => void;
  onSelectObject: (object: SceneObject) => void;
  onToggleVisibility: (type: 'projector' | 'camera' | 'object', id: number) => void;
  onDelete: (type: 'projector' | 'camera' | 'object', id: number) => void;
}

export const LeftPanel: React.FC<LeftPanelProps> = ({
  projectors,
  cameras,
  objects,
  selection,
  onSelectProjector,
  onSelectCamera,
  onSelectObject,
  onToggleVisibility,
  onDelete,
}) => {
  const [projectorsExpanded, setProjectorsExpanded] = useState(true);
  const [camerasExpanded, setCamerasExpanded] = useState(true);
  const [objectsExpanded, setObjectsExpanded] = useState(true);

  const isProjectorSelected = (p: ProjectorType) => 
    selection.type === 'projector' && (selection.instance as ProjectorType)?.id === p.id;
  
  const isCameraSelected = (c: Camera3D) => 
    selection.type === 'camera' && (selection.instance as Camera3D)?.id === c.id;
  
  const isObjectSelected = (o: SceneObject) => 
    selection.type === 'object' && (selection.instance as SceneObject)?.id === o.id;

  return (
    <div className="w-72 h-full overflow-y-auto bg-sidebar border-r border-border">
      {/* Search */}
      <div className="p-3 border-b border-border">
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">🔍</span>
          <input 
            type="text" 
            placeholder="Search..."
            className="control-input pl-9"
          />
        </div>
      </div>

      {/* Projectors Section */}
      <div className="control-panel m-2">
        <div 
          className="collapsible-header"
          onClick={() => setProjectorsExpanded(!projectorsExpanded)}
        >
          <div className="flex items-center gap-2 text-xs font-semibold text-primary uppercase">
            <Projector className="w-4 h-4" />
            <span>Projectors</span>
            <span className="text-muted-foreground">({projectors.length})</span>
          </div>
          <ChevronDown className={`chevron w-4 h-4 text-muted-foreground ${projectorsExpanded ? 'open' : ''}`} />
        </div>
        
        {projectorsExpanded && (
          <div className="p-2 space-y-1">
            {projectors.length === 0 ? (
              <div className="text-center py-6 text-muted-foreground text-xs">
                <Projector className="w-8 h-8 mx-auto mb-2 opacity-30" />
                <p>No projectors yet</p>
                <p className="text-xs mt-1">Click "+ Projector" to add one</p>
              </div>
            ) : (
              projectors.map(projector => (
                <div 
                  key={projector.id}
                  className={`hierarchy-item ${isProjectorSelected(projector) ? 'selected' : ''}`}
                  onClick={() => onSelectProjector(projector)}
                >
                  <span className="text-lg">📽️</span>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">{projector.config.name} #{projector.id}</div>
                    <div className="text-xs text-muted-foreground">{projector.config.lumens.toLocaleString()} lm</div>
                  </div>
                  <button 
                    className="p-1 hover:bg-accent rounded"
                    onClick={(e) => { e.stopPropagation(); onToggleVisibility('projector', projector.id); }}
                  >
                    <Eye className="w-3 h-3" />
                  </button>
                  <button 
                    className="p-1 hover:bg-destructive/20 rounded text-destructive"
                    onClick={(e) => { e.stopPropagation(); onDelete('projector', projector.id); }}
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
              ))
            )}
          </div>
        )}
      </div>

      {/* Cameras Section */}
      <div className="control-panel m-2">
        <div 
          className="collapsible-header"
          onClick={() => setCamerasExpanded(!camerasExpanded)}
        >
          <div className="flex items-center gap-2 text-xs font-semibold text-primary uppercase">
            <Camera className="w-4 h-4" />
            <span>Cameras</span>
            <span className="text-muted-foreground">({cameras.length})</span>
          </div>
          <ChevronDown className={`chevron w-4 h-4 text-muted-foreground ${camerasExpanded ? 'open' : ''}`} />
        </div>
        
        {camerasExpanded && (
          <div className="p-2 space-y-1">
            {cameras.length === 0 ? (
              <div className="text-center py-4 text-muted-foreground text-xs">
                <Camera className="w-6 h-6 mx-auto mb-2 opacity-30" />
                <p>No cameras</p>
              </div>
            ) : (
              cameras.map(camera => (
                <div 
                  key={camera.id}
                  className={`hierarchy-item ${isCameraSelected(camera) ? 'selected' : ''}`}
                  onClick={() => onSelectCamera(camera)}
                >
                  <span className="text-lg">📷</span>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">{camera.name}</div>
                    <div className="text-xs text-muted-foreground">
                      FOV: {camera.fov}° {camera.assignedToViewer ? '• Viewer' : ''}
                    </div>
                  </div>
                  <button 
                    className="p-1 hover:bg-accent rounded"
                    onClick={(e) => { e.stopPropagation(); onToggleVisibility('camera', camera.id); }}
                  >
                    <Eye className="w-3 h-3" />
                  </button>
                  <button 
                    className="p-1 hover:bg-destructive/20 rounded text-destructive"
                    onClick={(e) => { e.stopPropagation(); onDelete('camera', camera.id); }}
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
              ))
            )}
          </div>
        )}
      </div>

      {/* Objects Section */}
      <div className="control-panel m-2">
        <div 
          className="collapsible-header"
          onClick={() => setObjectsExpanded(!objectsExpanded)}
        >
          <div className="flex items-center gap-2 text-xs font-semibold text-primary uppercase">
            <Box className="w-4 h-4" />
            <span>Objects</span>
            <span className="text-muted-foreground">({objects.length})</span>
          </div>
          <ChevronDown className={`chevron w-4 h-4 text-muted-foreground ${objectsExpanded ? 'open' : ''}`} />
        </div>
        
        {objectsExpanded && (
          <div className="p-2 space-y-1">
            {objects.length === 0 ? (
              <div className="text-center py-4 text-muted-foreground text-xs">
                <Box className="w-6 h-6 mx-auto mb-2 opacity-30" />
                <p>No objects</p>
              </div>
            ) : (
              objects.map(obj => (
                <div 
                  key={obj.id}
                  className={`hierarchy-item ${isObjectSelected(obj) ? 'selected' : ''}`}
                  onClick={() => onSelectObject(obj)}
                >
                  <span className="text-lg">
                    {obj.type === 'wall' ? '🧱' : obj.type === 'screen' ? '📺' : '📦'}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">{obj.name}</div>
                    <div className="text-xs text-muted-foreground capitalize">{obj.type}</div>
                  </div>
                  <button 
                    className="p-1 hover:bg-accent rounded"
                    onClick={(e) => { e.stopPropagation(); onToggleVisibility('object', obj.id); }}
                  >
                    {obj.visible ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
                  </button>
                  <button 
                    className="p-1 hover:bg-destructive/20 rounded text-destructive"
                    onClick={(e) => { e.stopPropagation(); onDelete('object', obj.id); }}
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};
