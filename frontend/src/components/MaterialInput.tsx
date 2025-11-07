import { useState } from 'react';

interface MaterialInputProps {
  materials: string[];
  inventory: Record<string, number>;
  onUpdate: (material: string, quantity: number) => void;
}

export default function MaterialInput({ materials, inventory, onUpdate }: MaterialInputProps) {
  const [searchQuery, setSearchQuery] = useState('');
  
  const filteredMaterials = materials.filter(m =>
    m.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        placeholder="🔍 Material suchen..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        className="w-full mb-4 px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-orange-500 text-white placeholder-gray-400"
      />
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 max-h-96 overflow-y-auto">
        {filteredMaterials.map(material => (
          <div key={material} className="flex items-center gap-2 bg-gray-700 rounded p-2">
            <label className="text-sm flex-1 min-w-0 truncate">{material}:</label>
            <div className="flex items-center gap-1">
              <button
                onClick={() => onUpdate(material, (inventory[material] || 0) - 1)}
                className="bg-gray-600 hover:bg-gray-500 px-2 py-1 rounded text-sm"
              >
                -
              </button>
              <input
                type="number"
                value={inventory[material] || 0}
                onChange={(e) => onUpdate(material, parseInt(e.target.value) || 0)}
                className="w-16 px-2 py-1 bg-gray-600 rounded text-center text-sm"
                min="0"
              />
              <button
                onClick={() => onUpdate(material, (inventory[material] || 0) + 1)}
                className="bg-gray-600 hover:bg-gray-500 px-2 py-1 rounded text-sm"
              >
                +
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

