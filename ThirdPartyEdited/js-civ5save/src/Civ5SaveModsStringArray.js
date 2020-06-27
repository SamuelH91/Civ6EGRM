import Civ5SaveIntProperty from './Civ5SaveIntProperty';
import Civ5SaveStringProperty from './Civ5SaveStringProperty';

/**
 * @ignore
 */
export default class Civ5SaveModsStringArray {
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
        let modId = new Civ5SaveStringProperty(currentByteOffset, null, saveData);
        currentByteOffset += modId.length;

        // Not sure what these extra bytes represent
        currentByteOffset += 4;

        let modName = new Civ5SaveStringProperty(currentByteOffset, null, saveData);
        currentByteOffset += modName.length;

        this._array.push(modName.getValue(saveData));
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
