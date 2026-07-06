export async function retry(
  fn: () => Promise<any>,
  retries = 3
) {

  try {
    return await fn();
  } catch (error) {

    if (retries === 0) {
      throw error;
    }

    return retry(fn, retries - 1);

  }

}