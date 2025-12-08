import React, { useState } from 'react';
import { ChevronDown, Settings, Aperture, Move3D, Target, Sliders } from 'lucide-react';
import { Projector, Camera3D, Selection, LensConfig } from '@/types/mapping';
import { LENSES, PROJECTOR_DATABASE } from '@/lib/projectorDatabase';

interface RightPanelProps {
  selection: Selection;
  projectors: Projector[];
  onUpdateProjectorSettings: (projectorId: number, settings: Partial<Projector>) => void;
  onSetProjectorOrientation: (projectorId: number, orientation: 'portrait' | 'landscape') => void;
}

export const RightPanel: React.FC<RightPanelProps> = ({
  selection,
  projectors,
  onUpdateProjectorSettings,
  onSetProjectorOrientation,
}) => {
  const [lensExpanded, setLensExpanded] = useState(true);
  const [transformExpanded, setTransformExpanded] = useState(true);
  const [keystoneExpanded, setKeystoneExpanded] = useState(false);
  const [softEdgeExpanded, setSoftEdgeExpanded] = useState(false);

  const activeProjector = selection.type === 'projector' 
    ? selection.instance as Projector 
    : projectors[0] || null;

  if (!activeProjector) {
    return (
      <div className="w-80 h-full bg-sidebar border-l border-border flex items-center justify-center">
        <div className="text-center text-muted-foreground p-6">
          <Settings className="w-12 h-12 mx-auto mb-4 opacity-30" />
          <p className="text-sm">No projector selected</p>
          <p className="text-xs mt-2">Add a projector to configure settings</p>
        </div>
      </div>
    );
  }

  const config = activeProjector.config;
  const lens = activeProjector.currentLens;
  const compatibleLenses = config.compatibleLenses.map(id => LENSES[id]).filter(Boolean);

  const handleLensChange = (lensId: string) => {
    const newLens = LENSES[lensId];
    if (newLens) {
      onUpdateProjectorSettings(activeProjector.id, {
        currentLensId: lensId,
        currentLens: newLens,
        throwRatio: newLens.throwMin,
        lensShiftV: Math.max(newLens.shiftV[0], Math.min(newLens.shiftV[1], activeProjector.lensShiftV)),
        lensShiftH: Math.max(newLens.shiftH[0], Math.min(newLens.shiftH[1], activeProjector.lensShiftH)),
      });
    }
  };

  return (
    <div className="w-80 h-full overflow-y-auto bg-sidebar border-l border-border">
      {/* Projector Info */}
      <div className="p-4 border-b border-border bg-gradient-to-r from-primary/10 to-transparent">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center">
            <span className="text-xl">📽️</span>
          </div>
          <div>
            <div className="font-semibold text-sm">{config.name} #{activeProjector.id}</div>
            <div className="text-xs text-muted-foreground">{config.brand} • {config.lumens.toLocaleString()} lm</div>
          </div>
        </div>
        
        {/* Orientation Toggle */}
        <div className="mt-4 flex gap-2">
          <button 
            className={`flex-1 py-2 text-xs rounded-lg transition-all ${
              activeProjector.orientation === 'landscape' 
                ? 'bg-primary text-primary-foreground' 
                : 'bg-muted text-muted-foreground'
            }`}
            onClick={() => onSetProjectorOrientation(activeProjector.id, 'landscape')}
          >
            Landscape
          </button>
          <button 
            className={`flex-1 py-2 text-xs rounded-lg transition-all ${
              activeProjector.orientation === 'portrait' 
                ? 'bg-primary text-primary-foreground' 
                : 'bg-muted text-muted-foreground'
            }`}
            onClick={() => onSetProjectorOrientation(activeProjector.id, 'portrait')}
          >
            Portrait
          </button>
        </div>
      </div>

      {/* Throw Ratio Display */}
      <div className="p-3 bg-primary/5 border-b border-border">
        <div className="metric-display">
          <div className="metric-value">{activeProjector.throwRatio.toFixed(2)}:1</div>
          <div className="metric-label">Throw Ratio</div>
        </div>
      </div>

      {/* Lens & Position Section */}
      <div className="control-panel m-2">
        <div 
          className="collapsible-header"
          onClick={() => setLensExpanded(!lensExpanded)}
        >
          <div className="flex items-center gap-2 text-xs font-semibold text-primary uppercase">
            <Aperture className="w-4 h-4" />
            <span>Lens & Position</span>
          </div>
          <ChevronDown className={`chevron w-4 h-4 text-muted-foreground ${lensExpanded ? 'open' : ''}`} />
        </div>
        
        {lensExpanded && (
          <div className="panel-content">
            {/* Lens Selection */}
            <div>
              <label className="text-xs text-muted-foreground block mb-2">🔭 Lens</label>
              <select 
                className="control-select"
                value={activeProjector.currentLensId}
                onChange={(e) => handleLensChange(e.target.value)}
              >
                {compatibleLenses.map(l => (
                  <option key={l.id} value={l.id}>
                    {l.id} ({l.fixed ? `${l.throwMin}:1` : `${l.throwMin}-${l.throwMax}:1`})
                  </option>
                ))}
              </select>
              
              <div className="mt-2 p-2 bg-primary/5 rounded text-xs space-y-1">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Throw:</span>
                  <span className="text-primary">{lens.fixed ? `${lens.throwMin}:1` : `${lens.throwMin}-${lens.throwMax}:1`}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Shift V:</span>
                  <span className="text-primary">{lens.shiftV[0]}% to {lens.shiftV[1]}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Shift H:</span>
                  <span className="text-primary">{lens.shiftH[0]}% to {lens.shiftH[1]}%</span>
                </div>
              </div>
            </div>

            {/* Throw Ratio Slider */}
            <div>
              <label className="text-xs text-muted-foreground flex justify-between mb-2">
                <span>Throw Ratio</span>
                <span className="text-primary font-semibold">{activeProjector.throwRatio.toFixed(2)}:1</span>
              </label>
              <input 
                type="range"
                className="control-slider"
                min={lens.throwMin}
                max={lens.throwMax}
                step={0.01}
                value={activeProjector.throwRatio}
                disabled={lens.fixed}
                onChange={(e) => onUpdateProjectorSettings(activeProjector.id, { throwRatio: parseFloat(e.target.value) })}
              />
            </div>

            {/* Lens Shift V */}
            <div>
              <label className="text-xs text-muted-foreground flex justify-between mb-2">
                <span>Lens Shift Vertical</span>
                <span className="text-primary font-semibold">{activeProjector.lensShiftV}%</span>
              </label>
              <input 
                type="range"
                className="control-slider"
                min={lens.shiftV[0]}
                max={lens.shiftV[1]}
                step={1}
                value={activeProjector.lensShiftV}
                onChange={(e) => onUpdateProjectorSettings(activeProjector.id, { lensShiftV: parseInt(e.target.value) })}
              />
            </div>

            {/* Lens Shift H */}
            <div>
              <label className="text-xs text-muted-foreground flex justify-between mb-2">
                <span>Lens Shift Horizontal</span>
                <span className="text-primary font-semibold">{activeProjector.lensShiftH}%</span>
              </label>
              <input 
                type="range"
                className="control-slider"
                min={lens.shiftH[0]}
                max={lens.shiftH[1]}
                step={1}
                value={activeProjector.lensShiftH}
                onChange={(e) => onUpdateProjectorSettings(activeProjector.id, { lensShiftH: parseInt(e.target.value) })}
              />
            </div>

            {/* Intensity */}
            <div>
              <label className="text-xs text-muted-foreground flex justify-between mb-2">
                <span>Intensity</span>
                <span className="text-primary font-semibold">{activeProjector.projectionIntensity.toFixed(1)}</span>
              </label>
              <input 
                type="range"
                className="control-slider"
                min={0}
                max={2}
                step={0.1}
                value={activeProjector.projectionIntensity}
                onChange={(e) => onUpdateProjectorSettings(activeProjector.id, { projectionIntensity: parseFloat(e.target.value) })}
              />
            </div>

            {/* Target Lock */}
            <div className="flex items-center justify-between p-2 bg-muted/30 rounded">
              <div className="flex items-center gap-2">
                <Target className="w-4 h-4 text-primary" />
                <span className="text-xs">Lock Aim to Target</span>
              </div>
              <input 
                type="checkbox"
                checked={activeProjector.targetLocked}
                onChange={(e) => onUpdateProjectorSettings(activeProjector.id, { targetLocked: e.target.checked })}
                className="w-4 h-4 accent-primary"
              />
            </div>
          </div>
        )}
      </div>

      {/* Transform Section */}
      <div className="control-panel m-2">
        <div 
          className="collapsible-header"
          onClick={() => setTransformExpanded(!transformExpanded)}
        >
          <div className="flex items-center gap-2 text-xs font-semibold text-primary uppercase">
            <Move3D className="w-4 h-4" />
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
                  value={activeProjector.group.position.x.toFixed(2)}
                  step={0.1}
                  readOnly
                />
              </div>
              <div>
                <label className="text-[10px] text-muted-foreground block mb-1 text-center">Y</label>
                <input 
                  type="number"
                  className="control-input text-center text-xs"
                  value={activeProjector.group.position.y.toFixed(2)}
                  step={0.1}
                  readOnly
                />
              </div>
              <div>
                <label className="text-[10px] text-muted-foreground block mb-1 text-center">Z</label>
                <input 
                  type="number"
                  className="control-input text-center text-xs"
                  value={activeProjector.group.position.z.toFixed(2)}
                  step={0.1}
                  readOnly
                />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Keystone Section */}
      <div className="control-panel m-2">
        <div 
          className="collapsible-header"
          onClick={() => setKeystoneExpanded(!keystoneExpanded)}
        >
          <div className="flex items-center gap-2 text-xs font-semibold text-primary uppercase">
            <Sliders className="w-4 h-4" />
            <span>Keystone Correction</span>
          </div>
          <ChevronDown className={`chevron w-4 h-4 text-muted-foreground ${keystoneExpanded ? 'open' : ''}`} />
        </div>
        
        {keystoneExpanded && (
          <div className="panel-content">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-muted-foreground flex justify-between mb-1">
                  <span>Vertical</span>
                  <span className="text-primary">{activeProjector.keystoneV}</span>
                </label>
                <input 
                  type="range"
                  className="control-slider"
                  min={-50}
                  max={50}
                  value={activeProjector.keystoneV}
                  onChange={(e) => onUpdateProjectorSettings(activeProjector.id, { keystoneV: parseInt(e.target.value) })}
                />
              </div>
              <div>
                <label className="text-xs text-muted-foreground flex justify-between mb-1">
                  <span>Horizontal</span>
                  <span className="text-primary">{activeProjector.keystoneH}</span>
                </label>
                <input 
                  type="range"
                  className="control-slider"
                  min={-50}
                  max={50}
                  value={activeProjector.keystoneH}
                  onChange={(e) => onUpdateProjectorSettings(activeProjector.id, { keystoneH: parseInt(e.target.value) })}
                />
              </div>
            </div>
            
            <button 
              className="w-full py-2 text-xs bg-muted hover:bg-accent rounded mt-2"
              onClick={() => onUpdateProjectorSettings(activeProjector.id, { keystoneV: 0, keystoneH: 0 })}
            >
              Reset Keystone
            </button>
          </div>
        )}
      </div>

      {/* Soft Edge Section */}
      <div className="control-panel m-2">
        <div 
          className="collapsible-header"
          onClick={() => setSoftEdgeExpanded(!softEdgeExpanded)}
        >
          <div className="flex items-center gap-2 text-xs font-semibold text-primary uppercase">
            <Sliders className="w-4 h-4" />
            <span>Soft Edge Blending</span>
          </div>
          <ChevronDown className={`chevron w-4 h-4 text-muted-foreground ${softEdgeExpanded ? 'open' : ''}`} />
        </div>
        
        {softEdgeExpanded && (
          <div className="panel-content space-y-3">
            {['L', 'R', 'T', 'B'].map((edge) => {
              const key = `softEdge${edge}` as keyof Projector;
              const label = edge === 'L' ? 'Left' : edge === 'R' ? 'Right' : edge === 'T' ? 'Top' : 'Bottom';
              return (
                <div key={edge}>
                  <label className="text-xs text-muted-foreground flex justify-between mb-1">
                    <span>{label}</span>
                    <span className="text-primary">{activeProjector[key] as number}%</span>
                  </label>
                  <input 
                    type="range"
                    className="control-slider"
                    min={0}
                    max={50}
                    value={activeProjector[key] as number}
                    onChange={(e) => onUpdateProjectorSettings(activeProjector.id, { [key]: parseInt(e.target.value) })}
                  />
                </div>
              );
            })}
            
            <div>
              <label className="text-xs text-muted-foreground flex justify-between mb-1">
                <span>Gamma</span>
                <span className="text-primary">{activeProjector.softEdgeGamma.toFixed(1)}</span>
              </label>
              <input 
                type="range"
                className="control-slider"
                min={1}
                max={4}
                step={0.1}
                value={activeProjector.softEdgeGamma}
                onChange={(e) => onUpdateProjectorSettings(activeProjector.id, { softEdgeGamma: parseFloat(e.target.value) })}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
