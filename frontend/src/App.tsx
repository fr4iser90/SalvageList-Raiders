import { useState, useEffect } from 'react';
import type { Item, MaterialQuantity } from './types';
import MaterialSelector from './components/MaterialSelector';
import ItemResultCard from './components/ItemResultCard';

const STORAGE_KEY = 'arc-raiders-needed-materials';

// Parse recycle string like "1x Wires, 2x Metal Parts" into MaterialQuantity[]
function parseRecycleString(recycleStr: string): MaterialQuantity[] {
  if (recycleStr === 'Cannot be recycled' || !recycleStr) {
    return [];
  }
  
  const materials: MaterialQuantity[] = [];
  const parts = recycleStr.split(',').map(s => s.trim());
  
  for (const part of parts) {
    const match = part.match(/^(\d+)x\s+(.+)$/);
    if (match) {
      materials.push({
        material: match[2].trim(),
        quantity: parseInt(match[1], 10),
      });
    }
  }
  
  return materials;
}

// Get all unique materials from all items
function getAllMaterials(items: Item[]): string[] {
  const materialsSet = new Set<string>();
  
  items.forEach(item => {
    if (item.recycles && item.recycles !== 'Cannot be recycled') {
      const materials = parseRecycleString(item.recycles);
      materials.forEach(m => materialsSet.add(m.material));
    }
  });
  
  return Array.from(materialsSet).sort();
}

// Find items that produce a specific material
function findItemsProducingMaterial(items: Item[], material: string): Array<{
  item: Item;
  materialQuantity: number;
  itemsNeeded: number;
}> {
  const results: Array<{
    item: Item;
    materialQuantity: number;
    itemsNeeded: number;
  }> = [];
  
  items.forEach(item => {
    if (item.recycles && item.recycles !== 'Cannot be recycled') {
      const materials = parseRecycleString(item.recycles);
      const materialMatch = materials.find(m => m.material === material);
      
      if (materialMatch) {
        results.push({
          item,
          materialQuantity: materialMatch.quantity,
          itemsNeeded: 0, // Will be calculated based on needed quantity
        });
      }
    }
  });
  
  return results;
}

function App() {
  const [items, setItems] = useState<Item[]>([]);
  const [selectedMaterial, setSelectedMaterial] = useState<string>('');
  const [neededQuantity, setNeededQuantity] = useState<number>(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch('/items.json')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then(data => {
        console.log('Items loaded:', data.length);
        setItems(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Fehler beim Laden der Items:', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // Load saved material selection
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const data = JSON.parse(saved);
        setSelectedMaterial(data.material || '');
        setNeededQuantity(data.quantity || 1);
      } catch (e) {
        console.error('Fehler beim Laden aus LocalStorage:', e);
      }
    }
  }, []);

  // Save material selection
  useEffect(() => {
    if (selectedMaterial) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        material: selectedMaterial,
        quantity: neededQuantity,
      }));
    }
  }, [selectedMaterial, neededQuantity]);

  const allMaterials = getAllMaterials(items);
  const itemsProducingMaterial = selectedMaterial
    ? findItemsProducingMaterial(items, selectedMaterial)
    : [];

  // Calculate how many items are needed for each result
  const resultsWithCalculation = itemsProducingMaterial.map(result => ({
    ...result,
    itemsNeeded: Math.ceil(neededQuantity / result.materialQuantity),
  }));

  // Sort by efficiency (most material per item first, then by items needed)
  resultsWithCalculation.sort((a, b) => {
    // First sort by material quantity per item (descending)
    if (b.materialQuantity !== a.materialQuantity) {
      return b.materialQuantity - a.materialQuantity;
    }
    // Then by items needed (ascending)
    return a.itemsNeeded - b.itemsNeeded;
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Lade Items...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-red-500 text-xl">Fehler: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900">
      <header className="bg-gray-800 border-b border-gray-700 sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-orange-500">🎮 ARC RAIDERS ITEM TRACKER</h1>
          <div className="mt-2 text-sm text-gray-400">
            Finde welche Items du recyceln kannst, um benötigte Materialien zu bekommen
          </div>
        </div>
      </header>

      <div className="bg-gray-800 border-b border-gray-700 sticky top-[120px] z-10">
        <div className="container mx-auto px-4 py-4">
          <MaterialSelector
            materials={allMaterials}
            selectedMaterial={selectedMaterial}
            neededQuantity={neededQuantity}
            onMaterialChange={setSelectedMaterial}
            onQuantityChange={setNeededQuantity}
          />
        </div>
      </div>

      <main className="container mx-auto px-4 py-6">
        {selectedMaterial ? (
          <>
            <h2 className="text-xl font-bold mb-4">
              Items die <span className="text-orange-500">{selectedMaterial}</span> liefern:
            </h2>
            {resultsWithCalculation.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {resultsWithCalculation.map((result, index) => (
                  <ItemResultCard
                    key={`${result.item.name}-${index}`}
                    item={result.item}
                    material={selectedMaterial}
                    materialQuantity={result.materialQuantity}
                    itemsNeeded={result.itemsNeeded}
                    totalNeeded={neededQuantity}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                Keine Items gefunden die {selectedMaterial} liefern.
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-12 text-gray-400">
            Wähle ein Material aus, um zu sehen welche Items es liefern.
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
