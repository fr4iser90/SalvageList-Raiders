import type { Item } from '../types';
import { t } from '../i18n';
import {
  translateItemName,
  translateMaterialName,
  translateCategoryName,
  translateRarityName,
  materialTranslations,
} from '../translations';

interface ItemResultCardProps {
  item: Item;
  material: string;
  materialQuantity: number;
  language?: 'de' | 'en';
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
  language = 'de',
}: ItemResultCardProps) {
  const rarityColor = rarityColors[item.rarity] || 'bg-gray-500';
  
  // Translate names based on language
  const translatedItemName = translateItemName(item.name, language);
  const translatedRarity = translateRarityName(item.rarity, language);
  const translatedCategory = translateCategoryName(item.category, language);
  const translatedMaterial = translateMaterialName(material, language);
  
  // Translate recycle string
  const translateRecycleString = (recycleStr: string): string => {
    if (recycleStr === 'Cannot be recycled' || !recycleStr) {
      return language === 'de' ? 'Kann nicht recycelt werden' : recycleStr;
    }
    // Simple translation - replace material names in the string
    let translated = recycleStr;
    Object.entries(materialTranslations).forEach(([en, de]) => {
      if (language === 'de') {
        translated = translated.replace(new RegExp(en, 'g'), de);
      }
    });
    return translated;
  };

  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 transition-colors">
      <div className="flex items-center gap-3 mb-3">
        {item.image && !item.image.startsWith('data:') && (
          <img
            src={item.image}
            alt={translatedItemName}
            className="w-16 h-16 object-contain flex-shrink-0"
            onError={(e) => {
              (e.target as HTMLImageElement).style.display = 'none';
            }}
          />
        )}
        <div className="flex-1 min-w-0">
          <h3 className="font-bold text-sm truncate">{translatedItemName}</h3>
          <span className={`inline-block px-2 py-0.5 rounded text-xs font-semibold ${rarityColor}`}>
            {translatedRarity}
          </span>
        </div>
      </div>

      <div className="text-xs text-gray-400 mb-3">{translatedCategory}</div>

      <div className="bg-blue-900/30 border border-blue-700 rounded p-3 mb-3">
        <div className="text-blue-300 text-sm font-bold">
          {t('perItem', language, { quantity: materialQuantity.toString(), material: translatedMaterial })}
        </div>
      </div>

      <div className="text-xs text-gray-500 space-y-1">
        <div>{t('sell', language)}: {item.sell_price}</div>
        <div className="text-gray-400">{t('recyclesTo', language)}: {translateRecycleString(item.recycles)}</div>
      </div>
    </div>
  );
}

