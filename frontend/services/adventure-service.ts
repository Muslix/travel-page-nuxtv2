import type { AdventureResponse, Adventure } from '~/types/adventure';
import { useRuntimeConfig, useFetch } from '#imports';

// Service object for Adventure API endpoints
const adventureService = {
  async getAllAdventures() {
    const config = useRuntimeConfig();
    const baseURL = config.public.apiBase;
    try {
      const { data, error } = await useFetch<AdventureResponse>(
        `${baseURL}/api/adventures/`,
        { headers: { 'Content-Type': 'application/json' } }
      );
      if (error.value) {
        console.error('Error fetching adventures:', error.value);
        return { adventures: [], error: error.value };
      }
      return { adventures: data.value?.items || [], error: null };
    } catch (err) {
      console.error('Error in adventure service getAllAdventures:', err);
      return { adventures: [], error: err };
    }
  },

  async getAdventureById(id: string) {
    const config = useRuntimeConfig();
    const baseURL = config.public.apiBase;
    try {
      const { data, error } = await useFetch<Adventure>(
        `${baseURL}/api/adventures/${id}`,
        { headers: { 'Content-Type': 'application/json' } }
      );
      if (error.value) {
        console.error(`Error fetching adventure ${id}:`, error.value);
        return { adventure: null, error: error.value };
      }
      return { adventure: data.value, error: null };
    } catch (err) {
      console.error('Error in adventure service getAdventureById:', err);
      return { adventure: null, error: err };
    }
  },

  async getAdventureBySlug(slug: string) {
    const config = useRuntimeConfig();
    const baseURL = config.public.apiBase;
    try {
      const { data, error } = await useFetch<Adventure>(
        `${baseURL}/api/adventures/slug/${slug}`,
        { headers: { 'Content-Type': 'application/json' } }
      );
      if (error.value) {
        console.error(`Error fetching adventure with slug ${slug}:`, error.value);
        return { adventure: null, error: error.value };
      }
      return { adventure: data.value, error: null };
    } catch (err) {
      console.error('Error in adventure service getAdventureBySlug:', err);
      return { adventure: null, error: err };
    }
  },

  async getAdventures(params: { status?: string; limit?: number }) {
    const config = useRuntimeConfig();
    const baseURL = config.public.apiBase;
    try {
      const { data, error } = await useFetch<AdventureResponse>(
        `${baseURL}/api/adventures/`,
        { params, headers: { 'Content-Type': 'application/json' } }
      );
      if (error.value) {
        console.error('Error fetching adventures:', error.value);
        return { adventures: [], error: error.value };
      }
      return { adventures: data.value?.items || [], error: null };
    } catch (err) {
      console.error('Error in adventure service getAdventures:', err);
      return { adventures: [], error: err };
    }
  }
};

export default adventureService;
