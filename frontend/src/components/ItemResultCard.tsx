import type { Item } from '../types';

interface ItemResultCardProps {
  item: Item;
  material: string;
  materialQuantity: number;
  itemsNeeded: number;
  totalNeeded: number;
}

const rarityColors: Record<string, string> = {
  Common: 'bg-gray-500',
  Uncommon: 'bg-green-500',
  Rare: 'bg-blue-500',
  Epic: 'bg-purple-500',
  Legendary: 'bg-yellow-500',
  Uncomon: 'bg-green-500',
};

export default function ItemResultCard({
  item,
  material,
  materialQuantity,
  itemsNeeded,
  totalNeeded,
}: ItemResultCardProps) {
  const rarityColor = rarityColors[item.rarity] || 'bg-gray-500';
  const totalMaterialFromItems = itemsNeeded * materialQuantity;
  const efficiency = materialQuantity; // Higher is better

  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 transition-colors">
      <div className="flex items-center gap-3 mb-3">
        {item.image && !item.image.startsWith('data:') && (
          <img
            src={item.image}
            alt={item.name}
            className="w-16 h-16 object-contain flex-shrink-0"
            onError={(e) => {
              (e.target as HTMLImageElement).style.display = 'none';
            }}
          />
        )}
        <div className="flex-1 min-w-0">
          <h3 className="font-bold text-sm truncate">{item.name}</h3>
          <span className={`inline-block px-2 py-0.5 rounded text-xs font-semibold ${rarityColor}`}>
            {item.rarity}
          </span>
        </div>
      </div>

      <div className="text-xs text-gray-400 mb-3">{item.category}</div>

      <div className="bg-blue-900/30 border border-blue-700 rounded p-3 mb-3">
        <div className="text-blue-300 text-sm mb-1">
          <span className="font-bold">{materialQuantity}x {material}</span> pro Item
        </div>
        <div className="text-blue-200 font-bold">
          Brauche: <span className="text-orange-400">{itemsNeeded}x</span> Items
        </div>
        <div className="text-blue-300 text-xs mt-1">
          = {totalMaterialFromItems}x {material} total
        </div>
      </div>

      <div className="text-xs text-gray-500 space-y-1">
        <div>Sell: {item.sell_price}</div>
        <div className="text-gray-400">Recycelt zu: {item.recycles}</div>
      </div>
    </div>
  );
}

