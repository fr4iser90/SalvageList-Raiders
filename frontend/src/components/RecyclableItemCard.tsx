import type { RecyclableItem } from '../types';

interface RecyclableItemCardProps {
  recyclable: RecyclableItem;
}

const rarityColors: Record<string, string> = {
  Common: 'bg-gray-500',
  Uncommon: 'bg-green-500',
  Rare: 'bg-blue-500',
  Epic: 'bg-purple-500',
  Legendary: 'bg-yellow-500',
  Uncomon: 'bg-green-500',
};

export default function RecyclableItemCard({ recyclable }: RecyclableItemCardProps) {
  const { item, materials, canRecycle, recycleCount } = recyclable;
  const rarityColor = rarityColors[item.rarity] || 'bg-gray-500';

  return (
    <div className={`bg-gray-800 rounded-lg p-4 border transition-colors ${
      canRecycle && recycleCount > 0 
        ? 'border-green-600 hover:border-green-500' 
        : 'border-gray-700 hover:border-gray-600'
    }`}>
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

      {canRecycle && recycleCount > 0 ? (
        <div className="bg-green-900/30 border border-green-700 rounded p-2 mb-3">
          <div className="text-green-300 font-bold text-sm">
            ♻️ Kann {recycleCount}x recyceln
          </div>
        </div>
      ) : (
        <div className="bg-gray-700/30 border border-gray-600 rounded p-2 mb-3">
          <div className="text-gray-400 text-xs">
            Nicht genug Materialien
          </div>
        </div>
      )}

      <div className="text-xs text-gray-500 space-y-1 mb-2">
        <div className="font-semibold text-gray-400">Recycelt zu:</div>
        {materials.map((m, idx) => (
          <div key={idx} className="text-gray-400">
            {m.quantity}x {m.material}
          </div>
        ))}
      </div>

      <div className="text-xs text-gray-500">
        Sell: {item.sell_price}
      </div>
    </div>
  );
}

