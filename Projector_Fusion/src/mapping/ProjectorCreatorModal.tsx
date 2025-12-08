import React, { useState } from 'react';
import { X, Projector, Search, Calculator, Settings } from 'lucide-react';
import { PROJECTOR_DATABASE, LENSES, throwToFOV } from '@/lib/projectorDatabase';

interface ProjectorCreatorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreateProjector: (modelId: string, withTestPattern: boolean) => void;
}

export const ProjectorCreatorModal: React.FC<ProjectorCreatorModalProps> = ({
  isOpen,
  onClose,
  onCreateProjector,
}) => {
  const [selectedModel, setSelectedModel] = useState<string>('PT-RQ25K');
  const [searchQuery, setSearchQuery] = useState('');
  const [addTestPattern, setAddTestPattern] = useState(true);
  const [activeTab, setActiveTab] = useState<'library' | 'calculator'>('library');
  
  // Calculator state
  const [calcScreenWidth, setCalcScreenWidth] = useState(6);
  const [calcDistance, setCalcDistance] = useState(10);
  const [calcLumens, setCalcLumens] = useState(10000);

  if (!isOpen) return null;

  const projectorModels = Object.entries(PROJECTOR_DATABASE);
  const filteredModels = projectorModels.filter(([id, config]) => 
    config.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    config.brand.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const selectedConfig = PROJECTOR_DATABASE[selectedModel];
  const selectedLens = selectedConfig ? LENSES[selectedConfig.defaultLens] : null;

  // Calculator calculations
  const calculatedThrowRatio = calcDistance / calcScreenWidth;
  const calculatedFOV = throwToFOV(calculatedThrowRatio);
  const requiredLumens = Math.round(calcScreenWidth * 1.5 * 150); // ~150 lux per m²
  const recommendedProjectors = projectorModels.filter(([id, config]) => {
    const lens = LENSES[config.defaultLens];
    return config.lumens >= requiredLumens * 0.8 && 
           lens && calculatedThrowRatio >= lens.throwMin && calculatedThrowRatio <= lens.throwMax;
  });

  const handleCreate = () => {
    onCreateProjector(selectedModel, addTestPattern);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 backdrop-blur-sm">
      <div className="bg-card border border-border rounded-xl w-[900px] max-h-[80vh] overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-border bg-gradient-to-r from-primary/10 to-transparent">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center">
              <Projector className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h2 className="font-bold text-lg">Créer un Projecteur</h2>
              <p className="text-xs text-muted-foreground">Sélectionnez un modèle ou utilisez le calculateur</p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-muted rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-border">
          <button 
            className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 transition-all ${
              activeTab === 'library' ? 'bg-primary/10 text-primary border-b-2 border-primary' : 'text-muted-foreground hover:text-foreground'
            }`}
            onClick={() => setActiveTab('library')}
          >
            <Projector className="w-4 h-4" />
            Bibliothèque Projecteurs
          </button>
          <button 
            className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 transition-all ${
              activeTab === 'calculator' ? 'bg-primary/10 text-primary border-b-2 border-primary' : 'text-muted-foreground hover:text-foreground'
            }`}
            onClick={() => setActiveTab('calculator')}
          >
            <Calculator className="w-4 h-4" />
            Calculateur
          </button>
        </div>

        <div className="flex h-[500px]">
          {activeTab === 'library' ? (
            <>
              {/* Left: Projector List */}
              <div className="w-1/2 border-r border-border flex flex-col">
                {/* Search */}
                <div className="p-3 border-b border-border">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <input 
                      type="text"
                      placeholder="Rechercher un projecteur..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="control-input pl-10"
                    />
                  </div>
                </div>

                {/* List */}
                <div className="flex-1 overflow-y-auto p-2 space-y-1">
                  {filteredModels.map(([id, config]) => (
                    <button
                      key={id}
                      className={`w-full text-left p-3 rounded-lg transition-all ${
                        selectedModel === id 
                          ? 'bg-primary/20 border border-primary/50' 
                          : 'hover:bg-muted border border-transparent'
                      }`}
                      onClick={() => setSelectedModel(id)}
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded bg-muted flex items-center justify-center text-lg">
                          📽️
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="font-medium text-sm truncate">{config.name}</div>
                          <div className="text-xs text-muted-foreground">
                            {config.brand} • {config.lumens.toLocaleString()} lm • {config.resolution}
                          </div>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Right: Details & Options */}
              <div className="w-1/2 flex flex-col">
                {selectedConfig && selectedLens && (
                  <>
                    <div className="flex-1 p-4 overflow-y-auto space-y-4">
                      {/* Preview */}
                      <div className="aspect-video bg-gradient-to-br from-muted to-muted/50 rounded-lg flex items-center justify-center">
                        <div className="text-center">
                          <div className="text-5xl mb-2">📽️</div>
                          <div className="font-bold">{selectedConfig.name}</div>
                          <div className="text-sm text-muted-foreground">{selectedConfig.brand}</div>
                        </div>
                      </div>

                      {/* Specs */}
                      <div className="grid grid-cols-2 gap-3">
                        <div className="p-3 bg-muted/30 rounded-lg">
                          <div className="text-2xl font-bold text-primary">{selectedConfig.lumens.toLocaleString()}</div>
                          <div className="text-xs text-muted-foreground">Lumens</div>
                        </div>
                        <div className="p-3 bg-muted/30 rounded-lg">
                          <div className="text-2xl font-bold text-primary">{selectedConfig.resolution}</div>
                          <div className="text-xs text-muted-foreground">Résolution</div>
                        </div>
                        <div className="p-3 bg-muted/30 rounded-lg">
                          <div className="text-lg font-bold text-primary">
                            {selectedLens.fixed ? `${selectedLens.throwMin}:1` : `${selectedLens.throwMin}-${selectedLens.throwMax}:1`}
                          </div>
                          <div className="text-xs text-muted-foreground">Throw Ratio</div>
                        </div>
                        <div className="p-3 bg-muted/30 rounded-lg">
                          <div className="text-lg font-bold text-primary">
                            {selectedConfig.compatibleLenses.length}
                          </div>
                          <div className="text-xs text-muted-foreground">Optiques compatibles</div>
                        </div>
                      </div>

                      {/* Test Pattern Option */}
                      <label className="flex items-center gap-3 p-4 bg-primary/10 border border-primary/30 rounded-lg cursor-pointer hover:bg-primary/20 transition-all">
                        <input 
                          type="checkbox"
                          checked={addTestPattern}
                          onChange={(e) => setAddTestPattern(e.target.checked)}
                          className="w-5 h-5 accent-primary rounded"
                        />
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <span className="text-lg">🎯</span>
                            <span className="text-sm font-medium">Ajouter une mire de test</span>
                          </div>
                          <p className="text-xs text-muted-foreground mt-1">
                            Créer automatiquement un écran avec mire d'alignement
                          </p>
                        </div>
                      </label>
                    </div>
                  </>
                )}

                {/* Create Button */}
                <div className="p-4 border-t border-border">
                  <button 
                    className="w-full py-3 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-all flex items-center justify-center gap-2"
                    onClick={handleCreate}
                  >
                    <Projector className="w-4 h-4" />
                    Créer {selectedConfig?.name}
                  </button>
                </div>
              </div>
            </>
          ) : (
            /* Calculator Tab */
            <div className="w-full p-6 overflow-y-auto">
              <div className="max-w-2xl mx-auto space-y-6">
                {/* Input Parameters */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="p-4 bg-muted/30 rounded-lg">
                    <label className="text-xs text-muted-foreground block mb-2">Largeur écran (m)</label>
                    <input 
                      type="number"
                      value={calcScreenWidth}
                      onChange={(e) => setCalcScreenWidth(parseFloat(e.target.value) || 0)}
                      className="control-input text-2xl font-bold text-center"
                      step={0.5}
                      min={1}
                      max={50}
                    />
                  </div>
                  <div className="p-4 bg-muted/30 rounded-lg">
                    <label className="text-xs text-muted-foreground block mb-2">Distance (m)</label>
                    <input 
                      type="number"
                      value={calcDistance}
                      onChange={(e) => setCalcDistance(parseFloat(e.target.value) || 0)}
                      className="control-input text-2xl font-bold text-center"
                      step={0.5}
                      min={1}
                      max={100}
                    />
                  </div>
                  <div className="p-4 bg-muted/30 rounded-lg">
                    <label className="text-xs text-muted-foreground block mb-2">Lumens souhaités</label>
                    <input 
                      type="number"
                      value={calcLumens}
                      onChange={(e) => setCalcLumens(parseInt(e.target.value) || 0)}
                      className="control-input text-2xl font-bold text-center"
                      step={1000}
                      min={1000}
                      max={50000}
                    />
                  </div>
                </div>

                {/* Calculated Results */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="p-4 bg-primary/10 border border-primary/30 rounded-lg text-center">
                    <div className="text-3xl font-bold text-primary">{calculatedThrowRatio.toFixed(2)}:1</div>
                    <div className="text-xs text-muted-foreground mt-1">Throw Ratio requis</div>
                  </div>
                  <div className="p-4 bg-primary/10 border border-primary/30 rounded-lg text-center">
                    <div className="text-3xl font-bold text-primary">{calculatedFOV.toFixed(1)}°</div>
                    <div className="text-xs text-muted-foreground mt-1">FOV équivalent</div>
                  </div>
                  <div className="p-4 bg-primary/10 border border-primary/30 rounded-lg text-center">
                    <div className="text-3xl font-bold text-primary">{requiredLumens.toLocaleString()}</div>
                    <div className="text-xs text-muted-foreground mt-1">Lumens recommandés</div>
                  </div>
                </div>

                {/* Recommended Projectors */}
                <div>
                  <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
                    <Settings className="w-4 h-4 text-primary" />
                    Projecteurs recommandés ({recommendedProjectors.length})
                  </h3>
                  {recommendedProjectors.length > 0 ? (
                    <div className="space-y-2 max-h-48 overflow-y-auto">
                      {recommendedProjectors.map(([id, config]) => (
                        <button
                          key={id}
                          className={`w-full text-left p-3 rounded-lg transition-all flex items-center gap-3 ${
                            selectedModel === id 
                              ? 'bg-primary/20 border border-primary/50' 
                              : 'bg-muted/30 hover:bg-muted border border-transparent'
                          }`}
                          onClick={() => {
                            setSelectedModel(id);
                            setActiveTab('library');
                          }}
                        >
                          <span className="text-2xl">📽️</span>
                          <div className="flex-1">
                            <div className="font-medium">{config.name}</div>
                            <div className="text-xs text-muted-foreground">
                              {config.lumens.toLocaleString()} lm • {config.resolution}
                            </div>
                          </div>
                          <span className="text-xs text-primary">✓ Compatible</span>
                        </button>
                      ))}
                    </div>
                  ) : (
                    <div className="p-6 text-center text-muted-foreground bg-muted/20 rounded-lg">
                      <p className="text-sm">Aucun projecteur compatible trouvé</p>
                      <p className="text-xs mt-1">Ajustez les paramètres ou consultez la bibliothèque</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
