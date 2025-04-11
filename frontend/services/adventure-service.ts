// Service für die Kommunikation mit den Adventure-API-Endpunkten
import { useFetch } from 'nuxt/app';
import type { AdventureResponse, Adventure } from '~/types/adventure';

export default function useAdventureService() {
  const config = useRuntimeConfig();
  const baseURL = config.public.apiBase;

  const getAllAdventures = async () => {
    try {
      const { data, error } = await useFetch<AdventureResponse>(
        `${baseURL}/api/adventures/`,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (error.value) {
        console.error('Error fetching adventures:', error.value);
        return { adventures: [], error: error.value };
      }

      return { adventures: data.value?.items || [], error: null };
    } catch (err) {
      console.error('Error in adventure service:', err);
      return { adventures: [], error: err };
    }
  };

  const getAdventureById = async (id: string) => {
    try {
      const { data, error } = await useFetch<Adventure>(
        `${baseURL}/api/adventures/${id}`,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (error.value) {
        console.error(`Error fetching adventure ${id}:`, error.value);
        return { adventure: null, error: error.value };
      }

      return { adventure: data.value, error: null };
    } catch (err) {
      console.error('Error in adventure service:', err);
      return { adventure: null, error: err };
    }
  };

  const getAdventureBySlug = async (slug: string) => {
    try {
      const { data, error } = await useFetch<Adventure>(
        `${baseURL}/api/adventures/slug/${slug}`,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (error.value) {
        console.error(`Error fetching adventure with slug ${slug}:`, error.value);
        return { adventure: null, error: error.value };
      }

      return { adventure: data.value, error: null };
    } catch (err) {
      console.error('Error in adventure service:', err);
      return { adventure: null, error: err };
    }
  };

  return {
    getAllAdventures,
    getAdventureById,
    getAdventureBySlug
  };
}
