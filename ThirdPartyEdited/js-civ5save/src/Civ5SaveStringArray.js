import Civ5SaveStringProperty from './Civ5SaveStringProperty';

/**
 * @ignore
 */
export default class Civ5SaveStringArray {
  /**
   * @ignore
   */
  constructor(byteOffset, items, saveData) {
    /**
     * @ignore
     */
    this.byteOffset = byteOffset;
    /**
     * @private
     */
    this._array = new Array();

    let currentByteOffset = this.byteOffset;
    for (let i = 0; i < items; i++) {
      let arrayItem = new Civ5SaveStringProperty(currentByteOffset, null, saveData);
      currentByteOffset += arrayItem.length;
      this._array.push(arrayItem.getValue(saveData));
    }

    /**
     * @ignore
     */
    this.length = currentByteOffset - this.byteOffset;
    Object.freeze(this._array);
  }

  /**
   * @ignore
   */
  getArray() {
    return this._array;
  }
}
