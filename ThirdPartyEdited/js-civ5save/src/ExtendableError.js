/**
 * @ignore
 * @see https://stackoverflow.com/a/32749533/399105
 */
export default class ExtendableError extends Error {
  /**
   * @ignore
   */
  constructor(message) {
    super(message);
    /**
     * @ignore
     */
    this.name = this.constructor.name;
    if (typeof Error.captureStackTrace === 'function') {
      Error.captureStackTrace(this, this.constructor);
    } else {
      /**
       * @ignore
       */
      this.stack = (new Error(message)).stack;
    }
  }
}
