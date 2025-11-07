import { useState } from 'react';

interface MaterialSelectorProps {
  materials: string[];
  selectedMaterial: string;
  neededQuantity: number;
  onMaterialChange: (material: string) => void;
  onQuantityChange: (quantity: number) => void;
}

export default function MaterialSelector({
  materials,
  selectedMaterial,
  neededQuantity,
  onMaterialChange,
  onQuantityChange,
}: MaterialSelectorProps) {
  const [inputValue, setInputValue] = useState(selectedMaterial);
  const [showSuggestions, setShowSuggestions] = useState(false);
  
  const filteredSuggestions = materials.filter(m =>
    m.toLowerCase().includes(inputValue.toLowerCase())
  ).slice(0, 10);

  const handleInputChange = (value: string) => {
    setInputValue(value);
    setShowSuggestions(true);
    onMaterialChange(value);
  };

  const handleSuggestionClick = (material: string) => {
    setInputValue(material);
    setShowSuggestions(false);
    onMaterialChange(material);
  };

  return (
    <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
      <div className="flex-1 relative">
        <label className="block text-sm font-semibold mb-2">Material das ich brauche:</label>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => handleInputChange(e.target.value)}
          onFocus={() => setShowSuggestions(true)}
          placeholder="z.B. Wires, Metal Parts, Chemicals..."
          className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-orange-500 text-white placeholder-gray-400"
        />
        {showSuggestions && inputValue && filteredSuggestions.length > 0 && (
          <div className="absolute z-20 w-full mt-1 bg-gray-800 border border-gray-700 rounded-lg shadow-lg max-h-60 overflow-y-auto">
            {filteredSuggestions.map(material => (
              <button
                key={material}
                onClick={() => handleSuggestionClick(material)}
                className="w-full text-left px-4 py-2 hover:bg-gray-700 text-sm"
              >
                {material}
              </button>
            ))}
          </div>
        )}
      </div>
      
      {selectedMaterial && (
        <div>
          <label className="block text-sm font-semibold mb-2">Menge:</label>
          <div className="flex items-center gap-2">
            <button
              onClick={() => onQuantityChange(Math.max(1, neededQuantity - 1))}
              className="bg-gray-700 hover:bg-gray-600 px-3 py-2 rounded text-sm"
            >
              -
            </button>
            <input
              type="number"
              value={neededQuantity}
              onChange={(e) => onQuantityChange(Math.max(1, parseInt(e.target.value) || 1))}
              className="w-24 px-3 py-2 bg-gray-700 border border-gray-600 rounded text-center text-sm"
              min="1"
            />
            <button
              onClick={() => onQuantityChange(neededQuantity + 1)}
              className="bg-gray-700 hover:bg-gray-600 px-3 py-2 rounded text-sm"
            >
              +
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

