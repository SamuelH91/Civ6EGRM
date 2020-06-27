import Civ5SaveProperty from './Civ5SaveProperty';

/**
 * @ignore
 */
export default class Civ5SaveIntProperty extends Civ5SaveProperty {
  /**
   * @ignore
   */
  getValue(saveData) {
    if (this.length === 1) {
      return saveData.getUint8(this.byteOffset);
    } else if (this.length === 4) {
      return saveData.getUint32(this.byteOffset, true);
    }
  }

  /**
   * @ignore
   */
  setValue(saveData, newValue) {
    if (this.length === 1) {
      saveData.setUint8(this.byteOffset, newValue);
    } else if (this.length === 4) {
      saveData.setUint32(this.byteOffset, newValue, true);
    }
  }
}
