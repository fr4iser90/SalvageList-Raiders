interface FilterBarProps {
  categories: string[];
  rarities: string[];
  categoryFilter: string;
  rarityFilter: string;
  onCategoryChange: (category: string) => void;
  onRarityChange: (rarity: string) => void;
}

export default function FilterBar({
  categories,
  rarities,
  categoryFilter,
  rarityFilter,
  onCategoryChange,
  onRarityChange,
}: FilterBarProps) {
  return (
    <div className="flex flex-wrap gap-3">
      <div>
        <label className="text-sm text-gray-400 mr-2">Kategorie:</label>
        <select
          value={categoryFilter}
          onChange={(e) => onCategoryChange(e.target.value)}
          className="px-3 py-1 bg-gray-700 border border-gray-600 rounded text-sm focus:outline-none focus:border-orange-500"
        >
          <option value="all">Alle</option>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      <div>
        <label className="text-sm text-gray-400 mr-2">Rarity:</label>
        <select
          value={rarityFilter}
          onChange={(e) => onRarityChange(e.target.value)}
          className="px-3 py-1 bg-gray-700 border border-gray-600 rounded text-sm focus:outline-none focus:border-orange-500"
        >
          <option value="all">Alle</option>
          {rarities.map(rarity => (
            <option key={rarity} value={rarity}>{rarity}</option>
          ))}
        </select>
      </div>
    </div>
  );
}

