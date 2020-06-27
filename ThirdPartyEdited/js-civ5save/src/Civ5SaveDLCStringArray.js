import Civ5SaveIntProperty from './Civ5SaveIntProperty';
import Civ5SaveStringProperty from './Civ5SaveStringProperty';

/**
 * @ignore
 */
export default class Civ5SaveDLCStringArray {
  /**
   * @ignore
   */
  constructor(byteOffset, saveData) {
    /**
     * @ignore
     */
    this.byteOffset = byteOffset;
    /**
     * @ignore
     */
    this.length = 4;
    /**
     * @private
     */
    this._array = new Array();
    /**
     * @private
     */
    this._size = new Civ5SaveIntProperty(this.byteOffset, 4, saveData);

    if (this._getSize(saveData) > 0) {
      let currentByteOffset = this.byteOffset + 4;
      for (let i = 0; i < this._getSize(saveData); i++) {
        // Skip 16 byte unique identifier followed by 0100 0000
        currentByteOffset += 20;
        let dlcName = new Civ5SaveStringProperty(currentByteOffset, null, saveData);
        currentByteOffset += dlcName.length;

        this._array.push(dlcName.getValue(saveData));
      }

      this.length = currentByteOffset - this.byteOffset;
    }

    Object.freeze(this._array);
  }

  /**
   * @private
   */
  _getSize(saveData) {
    return this._size.getValue(saveData);
  }

  /**
   * @ignore
   */
  getArray() {
    return this._array;
  }
}
