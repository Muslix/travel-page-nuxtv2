export interface Tag {
  id: string;
  name: string;
  slug: string;
}

export interface Image {
  id: string;
  url: string;
  alt_text?: string;
  width?: number;
  height?: number;
  is_featured?: boolean;
}

export interface Adventure {
  id: string;
  title: string;
  slug: string;
  description: string;
  content: string;
  distance_km?: number;
  elevation_m?: number;
  duration_days?: number;
  difficulty?: string;
  featured_image_url?: string;
  images?: Image[];
  tags?: Tag[];
  route_gpx_url?: string;
  created_at: string;
  updated_at?: string;
  published_at?: string;
  is_published: boolean;
}

export interface AdventureResponse {
  items: Adventure[];
  total: number;
  page: number;
  size: number;
  pages: number;
}
