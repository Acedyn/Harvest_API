interface CacheEntry<T> {
  result: T | undefined;
  lastFetch: number;
}

interface Cache {
  [route: string]: CacheEntry<unknown>;
}

export const cache: Cache = {};

export async function cacheResult<T>(
  route: string,
  invalidate: number,
  fetchFunction: () => Promise<T>
): Promise<T> {
  if (!cache[route]) {
    cache[route] = { result: undefined, lastFetch: 0 };
  }

  if (Date.now() - cache[route].lastFetch > invalidate) {
    cache[route] = {
      lastFetch: Date.now(),
      result: await fetchFunction(),
    };
  }

  return cache[route].result as T;
}
