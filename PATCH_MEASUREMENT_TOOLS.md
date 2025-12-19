# PATCH - Outils de Mesure pour Simulateur de Projecteurs
# À ajouter au fichier projector_TIMELINE_PROJECTOR_FIX_3.html

## 1. AJOUTER DANS LE CSS (après la ligne ~200)

```css
/* === MEASUREMENT TOOLS === */
#measurement-panel {
    position: absolute;
    top: 60px;
    left: 20px;
    background: rgba(0,0,0,0.95);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 15px;
    width: 300px;
    max-height: calc(90vh - 60px);
    overflow-y: auto;
    font-size: 11px;
    display: none;
    z-index: 400;
}

#measurement-panel.active {
    display: block;
}

.measurement-mode {
    background: var(--muted);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 12px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: all 0.2s;
}

.measurement-mode:hover {
    background: var(--accent);
    border-color: var(--primary);
}

.measurement-mode.active {
    background: var(--primary);
    border-color: var(--primary-glow);
    color: var(--background);
}

.measurement-mode-title {
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.measurement-mode-desc {
    font-size: 9px;
    opacity: 0.7;
    line-height: 1.3;
}

.measurement-list {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid var(--border);
}

.measurement-item {
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 10px;
    margin-bottom: 8px;
    font-size: 10px;
}

.measurement-item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}

.measurement-item-type {
    font-weight: 600;
    color: var(--primary);
}

.measurement-item-actions {
    display: flex;
    gap: 4px;
}

.measurement-item-btn {
    background: transparent;
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 3px 6px;
    cursor: pointer;
    font-size: 9px;
    color: var(--foreground);
    transition: all 0.15s;
}

.measurement-item-btn:hover {
    background: var(--primary);
    border-color: var(--primary);
    color: var(--background);
}

.measurement-item-value {
    font-size: 14px;
    font-weight: 600;
    color: var(--primary-glow);
    margin: 4px 0;
}

.measurement-item-details {
    font-size: 9px;
    color: var(--muted-foreground);
    line-height: 1.4;
}

.measurement-controls {
    display: flex;
    gap: 6px;
    margin-top: 10px;
}

.measurement-btn {
    flex: 1;
    padding: 8px;
    background: var(--muted);
    border: 1px solid var(--border);
    border-radius: 4px;
    cursor: pointer;
    font-size: 10px;
    color: var(--foreground);
    transition: all 0.15s;
}

.measurement-btn:hover {
    background: var(--primary);
    border-color: var(--primary);
    color: var(--background);
}

.measurement-point-marker {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #ff0;
    border: 2px solid #fff;
    position: absolute;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 1000;
    box-shadow: 0 0 10px rgba(255,255,0,0.5);
}
```

## 2. AJOUTER DANS LE MENU (après la ligne ~3089, dans le menu "🛠️ Outils")

```html
<div class="dropdown-item" onclick="toggleMeasurementPanel()">
    <span>📏</span> Outils de Mesure
</div>
```

## 3. AJOUTER AVANT </body> (créer le panneau de mesure)

```html
<!-- MEASUREMENT PANEL -->
<div id="measurement-panel">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
        <h3 style="font-size: 13px; color: var(--primary); margin: 0;">📏 Outils de Mesure</h3>
        <button onclick="toggleMeasurementPanel()" style="background: transparent; border: none; color: var(--foreground); font-size: 18px; cursor: pointer; padding: 0; line-height: 1;">&times;</button>
    </div>

    <div id="measurement-modes">
        <div class="measurement-mode" onclick="activateMeasurementMode('distance')">
            <div class="measurement-mode-title">
                📐 Mesure 2 Points
            </div>
            <div class="measurement-mode-desc">
                Cliquez sur 2 points dans la scène pour mesurer la distance 3D
            </div>
        </div>

        <div class="measurement-mode" onclick="activateMeasurementMode('surface')">
            <div class="measurement-mode-title">
                📦 Mesure Surface (4 Points)
            </div>
            <div class="measurement-mode-desc">
                Cliquez sur 4 points pour définir une surface rectangulaire
            </div>
        </div>
    </div>

    <div class="measurement-list" id="measurement-list">
        <div style="font-size: 10px; color: var(--muted-foreground); margin-bottom: 10px;">
            📊 Mesures Enregistrées
        </div>
        <div id="measurements-container" style="min-height: 50px;">
            <div style="font-size: 9px; color: var(--muted-foreground); text-align: center; padding: 20px;">
                Aucune mesure enregistrée
            </div>
        </div>
    </div>

    <div class="measurement-controls">
        <button class="measurement-btn" onclick="clearAllMeasurements()">
            🗑️ Effacer Tout
        </button>
        <button class="measurement-btn" onclick="exportMeasurements()">
            💾 Exporter
        </button>
    </div>
</div>
```

## 4. AJOUTER DANS LE JAVASCRIPT (avant la dernière ligne </script>)

```javascript
// === MEASUREMENT TOOLS ===

let measurementMode = null; // 'distance' or 'surface'
let measurementPoints = [];
let measurementObjects = []; // THREE.js objects for visualization
let savedMeasurements = [];
let measurementIdCounter = 0;

// Toggle measurement panel
window.toggleMeasurementPanel = function() {
    const panel = document.getElementById('measurement-panel');
    panel.classList.toggle('active');
};

// Activate measurement mode
window.activateMeasurementMode = function(mode) {
    // Deactivate all modes first
    document.querySelectorAll('.measurement-mode').forEach(el => {
        el.classList.remove('active');
    });

    if (measurementMode === mode) {
        // Toggle off
        measurementMode = null;
        measurementPoints = [];
        clearTemporaryMeasurementVisuals();
        renderer.domElement.style.cursor = 'default';
    } else {
        // Activate new mode
        measurementMode = mode;
        measurementPoints = [];
        clearTemporaryMeasurementVisuals();

        // Highlight active mode
        event.target.closest('.measurement-mode').classList.add('active');
        renderer.domElement.style.cursor = 'crosshair';

        const modeNames = {
            'distance': 'Mesure 2 Points',
            'surface': 'Mesure Surface (4 Points)'
        };
        console.log(`📏 Mode activé: ${modeNames[mode]}`);
    }
};

// Handle click for measurement
function handleMeasurementClick(event) {
    if (!measurementMode) return;

    const rect = renderer.domElement.getBoundingClientRect();
    const mouse = new THREE.Vector2(
        ((event.clientX - rect.left) / rect.width) * 2 - 1,
        -((event.clientY - rect.top) / rect.height) * 2 + 1
    );

    raycaster.setFromCamera(mouse, camera);

    // Get all objects in scene
    const allObjects = [];
    scene.traverse((obj) => {
        if (obj.isMesh) allObjects.push(obj);
    });

    const intersects = raycaster.intersectObjects(allObjects, false);

    if (intersects.length > 0) {
        const point = intersects[0].point.clone();
        measurementPoints.push(point);

        // Visual feedback - add point marker
        addMeasurementPointMarker(point, measurementPoints.length);

        // Check if we have enough points
        if (measurementMode === 'distance' && measurementPoints.length === 2) {
            completeMeasurement();
        } else if (measurementMode === 'surface' && measurementPoints.length === 4) {
            completeMeasurement();
        }
    }
}

// Add visual point marker
function addMeasurementPointMarker(point, index) {
    const geometry = new THREE.SphereGeometry(0.1, 16, 16);
    const material = new THREE.MeshBasicMaterial({
        color: 0xffff00,
        depthTest: false,
        transparent: true,
        opacity: 0.8
    });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.copy(point);
    sphere.renderOrder = 999;
    scene.add(sphere);
    measurementObjects.push(sphere);

    // Add label
    const canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 128;
    const context = canvas.getContext('2d');
    context.fillStyle = '#ffff00';
    context.font = 'Bold 64px Arial';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText(index.toString(), 64, 64);

    const texture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({
        map: texture,
        depthTest: false,
        sizeAttenuation: false
    });
    const sprite = new THREE.Sprite(spriteMaterial);
    sprite.scale.set(0.05, 0.05, 1);
    sprite.position.copy(point);
    sprite.position.y += 0.3;
    sprite.renderOrder = 1000;
    scene.add(sprite);
    measurementObjects.push(sprite);

    // Draw line between points
    if (measurementPoints.length > 1) {
        const lineGeometry = new THREE.BufferGeometry().setFromPoints([
            measurementPoints[measurementPoints.length - 2],
            point
        ]);
        const lineMaterial = new THREE.LineBasicMaterial({
            color: 0xffff00,
            linewidth: 2,
            depthTest: false
        });
        const line = new THREE.Line(lineGeometry, lineMaterial);
        line.renderOrder = 998;
        scene.add(line);
        measurementObjects.push(line);
    }
}

// Complete measurement
function completeMeasurement() {
    let result = null;

    if (measurementMode === 'distance') {
        const p1 = measurementPoints[0];
        const p2 = measurementPoints[1];
        const distance = p1.distanceTo(p2);

        result = {
            id: measurementIdCounter++,
            type: 'distance',
            value: distance,
            points: [p1.clone(), p2.clone()],
            timestamp: new Date().toLocaleString('fr-FR')
        };

        console.log(`📏 Distance: ${distance.toFixed(3)}m`);
    } else if (measurementMode === 'surface') {
        const [p1, p2, p3, p4] = measurementPoints;

        // Calculate distances
        const d12 = p1.distanceTo(p2);
        const d23 = p2.distanceTo(p3);
        const d34 = p3.distanceTo(p4);
        const d41 = p4.distanceTo(p1);
        const d13 = p1.distanceTo(p3);
        const d24 = p2.distanceTo(p4);

        // Calculate area using cross product (for planar quad)
        const v1 = new THREE.Vector3().subVectors(p2, p1);
        const v2 = new THREE.Vector3().subVectors(p4, p1);
        const v3 = new THREE.Vector3().subVectors(p3, p2);
        const v4 = new THREE.Vector3().subVectors(p4, p2);

        const area1 = new THREE.Vector3().crossVectors(v1, v2).length() / 2;
        const area2 = new THREE.Vector3().crossVectors(v3, v4).length() / 2;
        const totalArea = area1 + area2;

        const perimeter = d12 + d23 + d34 + d41;

        result = {
            id: measurementIdCounter++,
            type: 'surface',
            area: totalArea,
            perimeter: perimeter,
            distances: { d12, d23, d34, d41, d13, d24 },
            points: measurementPoints.map(p => p.clone()),
            timestamp: new Date().toLocaleString('fr-FR')
        };

        console.log(`📦 Surface: ${totalArea.toFixed(3)}m² | Périmètre: ${perimeter.toFixed(3)}m`);

        // Draw the surface
        drawSurfaceMeasurement(measurementPoints);
    }

    // Save measurement
    savedMeasurements.push(result);
    updateMeasurementsList();

    // Reset for new measurement
    measurementPoints = [];
}

// Draw surface visualization
function drawSurfaceMeasurement(points) {
    // Create a semi-transparent plane
    const shape = new THREE.Shape();
    shape.moveTo(0, 0);
    for (let i = 1; i < points.length; i++) {
        const localPoint = new THREE.Vector3()
            .subVectors(points[i], points[0]);
        shape.lineTo(localPoint.x, localPoint.z);
    }
    shape.lineTo(0, 0);

    const geometry = new THREE.ShapeGeometry(shape);
    const material = new THREE.MeshBasicMaterial({
        color: 0x00ff00,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.2,
        depthTest: false
    });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.copy(points[0]);
    mesh.renderOrder = 997;
    scene.add(mesh);
    measurementObjects.push(mesh);

    // Close the loop
    const lineGeometry = new THREE.BufferGeometry().setFromPoints([
        points[points.length - 1],
        points[0]
    ]);
    const lineMaterial = new THREE.LineBasicMaterial({
        color: 0xffff00,
        linewidth: 2,
        depthTest: false
    });
    const line = new THREE.Line(lineGeometry, lineMaterial);
    line.renderOrder = 998;
    scene.add(line);
    measurementObjects.push(line);
}

// Clear temporary visuals
function clearTemporaryMeasurementVisuals() {
    measurementObjects.forEach(obj => {
        scene.remove(obj);
        if (obj.geometry) obj.geometry.dispose();
        if (obj.material) {
            if (obj.material.map) obj.material.map.dispose();
            obj.material.dispose();
        }
    });
    measurementObjects = [];
}

// Update measurements list
function updateMeasurementsList() {
    const container = document.getElementById('measurements-container');

    if (savedMeasurements.length === 0) {
        container.innerHTML = `
            <div style="font-size: 9px; color: var(--muted-foreground); text-align: center; padding: 20px;">
                Aucune mesure enregistrée
            </div>
        `;
        return;
    }

    container.innerHTML = savedMeasurements.map(m => {
        if (m.type === 'distance') {
            return `
                <div class="measurement-item">
                    <div class="measurement-item-header">
                        <span class="measurement-item-type">📐 Distance #${m.id}</span>
                        <div class="measurement-item-actions">
                            <button class="measurement-item-btn" onclick="deleteMeasurement(${m.id})">🗑️</button>
                        </div>
                    </div>
                    <div class="measurement-item-value">${m.value.toFixed(3)} m</div>
                    <div class="measurement-item-details">
                        📅 ${m.timestamp}
                    </div>
                </div>
            `;
        } else if (m.type === 'surface') {
            return `
                <div class="measurement-item">
                    <div class="measurement-item-header">
                        <span class="measurement-item-type">📦 Surface #${m.id}</span>
                        <div class="measurement-item-actions">
                            <button class="measurement-item-btn" onclick="deleteMeasurement(${m.id})">🗑️</button>
                        </div>
                    </div>
                    <div class="measurement-item-value">${m.area.toFixed(3)} m²</div>
                    <div class="measurement-item-details">
                        Périmètre: ${m.perimeter.toFixed(3)} m<br>
                        Côtés: ${m.distances.d12.toFixed(2)}m × ${m.distances.d23.toFixed(2)}m × ${m.distances.d34.toFixed(2)}m × ${m.distances.d41.toFixed(2)}m<br>
                        📅 ${m.timestamp}
                    </div>
                </div>
            `;
        }
    }).join('');
}

// Delete measurement
window.deleteMeasurement = function(id) {
    savedMeasurements = savedMeasurements.filter(m => m.id !== id);
    updateMeasurementsList();
};

// Clear all measurements
window.clearAllMeasurements = function() {
    if (confirm('Effacer toutes les mesures enregistrées ?')) {
        savedMeasurements = [];
        clearTemporaryMeasurementVisuals();
        updateMeasurementsList();
    }
};

// Export measurements
window.exportMeasurements = function() {
    if (savedMeasurements.length === 0) {
        alert('Aucune mesure à exporter');
        return;
    }

    let csvContent = 'Type,Valeur,Unité,Détails,Date\n';

    savedMeasurements.forEach(m => {
        if (m.type === 'distance') {
            csvContent += `Distance,${m.value.toFixed(3)},m,"P1-P2",${m.timestamp}\n`;
        } else if (m.type === 'surface') {
            csvContent += `Surface,${m.area.toFixed(3)},m²,"Périmètre: ${m.perimeter.toFixed(3)}m",${m.timestamp}\n`;
        }
    });

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `mesures_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);

    console.log('📊 Mesures exportées');
};

// Hook into existing click handler
const originalOnClick = renderer.domElement.onclick;
renderer.domElement.addEventListener('click', handleMeasurementClick, false);
```

## 5. INSTRUCTIONS D'INSTALLATION

1. Ouvrir `projector_TIMELINE_PROJECTOR_FIX_3.html` dans un éditeur de texte
2. Ajouter le CSS à la fin de la section `<style>` (avant `</style>`)
3. Ajouter le menu dans la section "🛠️ Outils"
4. Ajouter le panneau HTML avant `</body>`
5. Ajouter le JavaScript avant la dernière balise `</script>`
6. Sauvegarder et tester!

## UTILISATION

1. Cliquer sur **🛠️ Outils** → **📏 Outils de Mesure**
2. Choisir **Mesure 2 Points** ou **Mesure Surface**
3. Cliquer dans la scène 3D sur les objets
4. Les mesures s'enregistrent automatiquement
5. Exporter en CSV si nécessaire

## FONCTIONNALITÉS

✅ Mesure distance 3D entre 2 points
✅ Mesure surface rectangulaire (4 points)
✅ Visualisation 3D avec lignes et points jaunes
✅ Liste des mesures sauvegardées
✅ Export CSV des mesures
✅ Suppression individuelle ou totale
✅ Timestamps sur chaque mesure
