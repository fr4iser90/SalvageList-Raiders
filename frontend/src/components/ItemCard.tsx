import type { Item, ItemState } from '../types';

interface ItemCardProps {
  item: Item;
  state: ItemState;
  onUpdate: (field: 'needed' | 'have', value: number) => void;
}

const rarityColors: Record<string, string> = {
  Common: 'bg-gray-500',
  Uncommon: 'bg-green-500',
  Rare: 'bg-blue-500',
  Epic: 'bg-purple-500',
  Legendary: 'bg-yellow-500',
  Uncomon: 'bg-green-500',
};

export default function ItemCard({ item, state, onUpdate }: ItemCardProps) {
  const canRecycle = state.have > state.needed;
  const recycleAmount = canRecycle ? state.have - state.needed : 0;
  const rarityColor = rarityColors[item.rarity] || 'bg-gray-500';

  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 transition-colors">
      <div className="flex items-center gap-3 mb-3">
        {item.image && (
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

      <div className="space-y-2 mb-3">
        <div className="flex items-center gap-2">
          <label className="text-sm w-20">Brauche:</label>
          <div className="flex items-center gap-1 flex-1">
            <button
              onClick={() => onUpdate('needed', state.needed - 1)}
              className="bg-gray-700 hover:bg-gray-600 px-2 py-1 rounded text-sm"
            >
              -
            </button>
            <input
              type="number"
              value={state.needed}
              onChange={(e) => onUpdate('needed', parseInt(e.target.value) || 0)}
              className="w-16 px-2 py-1 bg-gray-700 rounded text-center text-sm"
              min="0"
            />
            <button
              onClick={() => onUpdate('needed', state.needed + 1)}
              className="bg-gray-700 hover:bg-gray-600 px-2 py-1 rounded text-sm"
            >
              +
            </button>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-sm w-20">Habe:</label>
          <div className="flex items-center gap-1 flex-1">
            <button
              onClick={() => onUpdate('have', state.have - 1)}
              className="bg-gray-700 hover:bg-gray-600 px-2 py-1 rounded text-sm"
            >
              -
            </button>
            <input
              type="number"
              value={state.have}
              onChange={(e) => onUpdate('have', parseInt(e.target.value) || 0)}
              className="w-16 px-2 py-1 bg-gray-700 rounded text-center text-sm"
              min="0"
            />
            <button
              onClick={() => onUpdate('have', state.have + 1)}
              className="bg-gray-700 hover:bg-gray-600 px-2 py-1 rounded text-sm"
            >
              +
            </button>
          </div>
        </div>
      </div>

      {canRecycle && (
        <div className="bg-blue-900/30 border border-blue-700 rounded p-2 text-sm text-blue-300">
          ♻️ Kann {recycleAmount}x recyceln
        </div>
      )}

      <div className="mt-3 text-xs text-gray-500 space-y-1">
        <div>Sell: {item.sell_price}</div>
        {item.recycles !== 'Cannot be recycled' && (
          <div className="text-gray-400">→ {item.recycles}</div>
        )}
      </div>
    </div>
  );
}

