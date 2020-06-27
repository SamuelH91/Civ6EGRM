import Civ5SaveProperty from './Civ5SaveProperty';

/**
 * @ignore
 */
export default class Civ5SaveStringProperty extends Civ5SaveProperty {
  /**
   * @ignore
   */
  constructor(byteOffset, length, saveData) {
    super(byteOffset, length);

    if (this._isNullOrUndefined(this.length)) {
      /**
       * @ignore
       */
      this.length = this._getStringLength(saveData, this.byteOffset) + 4;
    }
  }

  /**
   * @private
   */
  _isNullOrUndefined(variable) {
    return typeof variable === 'undefined' || variable === null;
  }

  /**
   * @private
   */
  _getStringLength(saveData, byteOffset) {
    return saveData.getUint32(byteOffset, true);
  }

  /**
   * @ignore
   */
  getValue(saveData) {
    return saveData.getString(this.byteOffset + 4, this.length - 4);
  }
}
