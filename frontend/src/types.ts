export interface Item {
  name: string;
  rarity: 'Common' | 'Uncommon' | 'Rare' | 'Epic' | 'Legendary' | 'Uncomon';
  recycles: string;
  sell_price: string;
  category: string;
  image?: string;
  url?: string;
  keep_for_workshop?: string;
  keep_for_quests?: string;
}

export interface MaterialQuantity {
  material: string;
  quantity: number;
}
