export default class Request {
  static post = async (url, data) => {
    try {
      const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' },
      });
      const result = await response.text();
      return JSON.parse(result);
    } catch (error) {
      throw new Error(error);
    }
  };
}