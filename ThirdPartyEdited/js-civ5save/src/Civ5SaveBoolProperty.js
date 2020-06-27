import Civ5SaveProperty from './Civ5SaveProperty';

/**
 * @ignore
 */
export default class Civ5SaveBoolProperty extends Civ5SaveProperty {
  /**
   * @ignore
   */
  getValue(saveData) {
    if (this.length === 1) {
      return Boolean(saveData.getUint8(this.byteOffset));
    } else if (this.length === 4) {
      return Boolean(saveData.getUint32(this.byteOffset, true));
    }
  }

  /**
   * @ignore
   */
  setValue(saveData, newValue) {
    if (this.length === 1) {
      saveData.setUint8(this.byteOffset, Number(newValue));
    } else if (this.length === 4) {
      saveData.setUint32(this.byteOffset, Number(newValue), true);
    }
  }
}
