import React, { useRef, useState, useCallback, useEffect } from 'react';
import { Toaster } from '@/components/ui/toaster';
import { useToast } from '@/hooks/use-toast';
import { useSceneManager } from '@/hooks/useSceneManager';
import { TopMenuBar } from '@/components/mapping/TopMenuBar';
import { LeftPanel } from '@/components/mapping/LeftPanel';
import { RightPanel } from '@/components/mapping/RightPanel';
import { CameraPropertiesPanel } from '@/components/mapping/CameraPropertiesPanel';
import { TimelinePanel } from '@/components/mapping/TimelinePanel';
import { ProjectorCreatorModal } from '@/components/mapping/ProjectorCreatorModal';
import { Projector as ProjectorType, Camera3D, SceneObject } from '@/types/mapping';

const CameraMapping = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();
  
  const [timelineVisible, setTimelineVisible] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [showProjectorModal, setShowProjectorModal] = useState(false);

  const sceneManager = useSceneManager({ containerRef });

  // Handle raycasting selection
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleSceneClick = (e: Event) => {
      const customEvent = e as CustomEvent;
      if (customEvent.detail) {
        sceneManager.selectObject(customEvent.detail);
      }
    };

    container.addEventListener('scene-object-clicked', handleSceneClick);
    return () => container.removeEventListener('scene-object-clicked', handleSceneClick);
  }, [sceneManager]);

  const handleCreateProjector = useCallback((modelId: string, withTestPattern: boolean) => {
    try {
      const projector = sceneManager.addProjector(modelId, withTestPattern);
      toast({ title: "Projecteur créé", description: `${modelId} ajouté${withTestPattern ? ' avec mire' : ''}` });
    } catch (e) {
      toast({ title: "Erreur", description: "Échec création projecteur", variant: "destructive" });
    }
  }, [sceneManager, toast]);

  const handleAddCamera = useCallback(() => {
    try {
      sceneManager.addCamera();
      toast({ title: "Caméra ajoutée", description: "Nouvelle caméra dans la scène" });
    } catch (e) {
      toast({ title: "Erreur", description: "Échec ajout caméra", variant: "destructive" });
    }
  }, [sceneManager, toast]);

  const handleAddPrimitive = useCallback((type: 'box' | 'plane' | 'sphere' | 'cylinder' | 'cone') => {
    try {
      sceneManager.addPrimitive(type);
      toast({ title: "Objet ajouté", description: `${type} ajouté à la scène` });
    } catch (e) {
      toast({ title: "Erreur", description: "Échec ajout objet", variant: "destructive" });
    }
  }, [sceneManager, toast]);

  const handleAddWall = useCallback(() => {
    try {
      sceneManager.addWall();
      toast({ title: "Mur ajouté", description: "Écran de projection ajouté" });
    } catch (e) {
      toast({ title: "Erreur", description: "Échec ajout mur", variant: "destructive" });
    }
  }, [sceneManager, toast]);

  const handleLoadContent = useCallback(() => fileInputRef.current?.click(), []);

  const handleFileChange = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      try {
        await sceneManager.loadContent(file);
        toast({ title: "Contenu chargé", description: file.name });
      } catch (e) {
        toast({ title: "Erreur", description: "Échec chargement", variant: "destructive" });
      }
    }
  }, [sceneManager, toast]);

  const handleSelectProjector = useCallback((p: ProjectorType) => sceneManager.selectObject(p.mesh), [sceneManager]);
  const handleSelectCamera = useCallback((c: Camera3D) => sceneManager.selectObject(c.mesh), [sceneManager]);
  const handleSelectObject = useCallback((o: SceneObject) => sceneManager.selectObject(o.mesh as any), [sceneManager]);

  const handlePlay = useCallback(() => { setIsPlaying(true); sceneManager.contentVideo?.play(); }, [sceneManager]);
  const handlePause = useCallback(() => { setIsPlaying(false); sceneManager.contentVideo?.pause(); }, [sceneManager]);

  const selectedCamera = sceneManager.selection.type === 'camera' ? sceneManager.selection.instance as Camera3D : null;

  return (
    <div className="h-screen w-screen flex flex-col overflow-hidden bg-background">
      <input ref={fileInputRef} type="file" accept="image/*,video/*" className="hidden" onChange={handleFileChange} />

      <TopMenuBar 
        onAddProjector={() => setShowProjectorModal(true)}
        onAddCamera={handleAddCamera}
        onAddPrimitive={handleAddPrimitive}
        onAddWall={handleAddWall}
        onLoadContent={handleLoadContent}
        onExport={() => toast({ title: "Export", description: "Export PNG sequence" })}
        onToggleRecording={() => { setIsRecording(!isRecording); toast({ title: isRecording ? "Arrêt" : "Enregistrement" }); }}
        onPlay={handlePlay}
        onPause={handlePause}
        onSetTransformMode={sceneManager.setTransformMode}
        onToggleGrid={sceneManager.toggleGrid}
        onSetCameraView={sceneManager.setCameraView}
        onDelete={sceneManager.deleteSelected}
        transformMode={sceneManager.transformMode}
        isRecording={isRecording}
        isPlaying={isPlaying}
        hasSelection={sceneManager.selection.object !== null}
      />

      <div className="flex-1 flex overflow-hidden">
        <LeftPanel 
          projectors={sceneManager.projectors}
          cameras={sceneManager.cameras}
          objects={sceneManager.objects}
          selection={sceneManager.selection}
          onSelectProjector={handleSelectProjector}
          onSelectCamera={handleSelectCamera}
          onSelectObject={handleSelectObject}
          onToggleVisibility={() => {}}
          onDelete={() => sceneManager.deleteSelected()}
        />

        <div className="flex-1 flex flex-col relative">
          <div ref={containerRef} className="flex-1 viewport-container" />

          {/* Preview Windows */}
          <div className="absolute bottom-4 right-4 flex gap-3 z-10">
            <div className="preview-window w-64">
              <div className="preview-label text-[10px]">📽️ Projector Output</div>
              <div className="aspect-video bg-black/80 flex items-center justify-center text-muted-foreground text-xs">
                {sceneManager.projectorViewCamera ? sceneManager.projectorViewCamera.name : 
                  (sceneManager.projectors.length > 0 ? 'Projector View' : 'No Projector')}
              </div>
            </div>
            <div className="preview-window w-64">
              <div className="preview-label-secondary text-[10px]">🎥 Mapping Preview</div>
              <div className="aspect-video bg-black/80 flex items-center justify-center text-muted-foreground text-xs">
                {sceneManager.mappingPreviewCamera ? sceneManager.mappingPreviewCamera.name : 'Main View'}
              </div>
            </div>
          </div>
        </div>

        {/* Right Panel - Camera or Projector properties */}
        {selectedCamera ? (
          <CameraPropertiesPanel
            camera={selectedCamera}
            onUpdateCamera={sceneManager.updateCameraSettings}
            onAssignToProjectorView={sceneManager.assignCameraToProjectorView}
            onAssignToMappingPreview={sceneManager.assignCameraToMappingPreview}
            assignedToProjectorView={selectedCamera.assignedToProjectorView}
            assignedToMappingPreview={selectedCamera.assignedToMappingPreview}
          />
        ) : (
          <RightPanel 
            selection={sceneManager.selection}
            projectors={sceneManager.projectors}
            onUpdateProjectorSettings={sceneManager.updateProjectorSettings}
            onSetProjectorOrientation={sceneManager.setProjectorOrientation}
          />
        )}
      </div>

      <TimelinePanel 
        timeline={sceneManager.timeline}
        onPlayPause={() => isPlaying ? handlePause() : handlePlay()}
        onSeek={() => {}}
        onAddKeyframe={() => toast({ title: "Keyframe", description: "Appuyez K avec objet sélectionné" })}
        onToggleLayerVisibility={() => {}}
        onToggleLayerLock={() => {}}
        visible={timelineVisible}
        onToggleVisibility={() => setTimelineVisible(!timelineVisible)}
      />

      <ProjectorCreatorModal
        isOpen={showProjectorModal}
        onClose={() => setShowProjectorModal(false)}
        onCreateProjector={handleCreateProjector}
      />

      <Toaster />
    </div>
  );
};

export default CameraMapping;
