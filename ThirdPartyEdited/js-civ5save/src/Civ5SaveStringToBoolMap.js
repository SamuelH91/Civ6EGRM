import Civ5SaveBoolProperty from './Civ5SaveBoolProperty';
import Civ5SaveDataView from './Civ5SaveDataView';
import Civ5SaveIntProperty from './Civ5SaveIntProperty';
import Civ5SaveStringProperty from './Civ5SaveStringProperty';

/**
 * @ignore
 */
export default class Civ5SaveStringToBoolMap {
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
    this._items = new Map();
    /**
     * @private
     */
    this._size = new Civ5SaveIntProperty(this.byteOffset, 4, saveData);

    if (this._getSize(saveData) > 0) {
      let currentByteOffset = this.byteOffset + 4;
      for (let i = 0; i < this._getSize(saveData); i++) {
        currentByteOffset = this._addItemToMap(saveData, currentByteOffset);
      }
    }
  }

  /**
   * @private
   */
  _addItemToMap(saveData, byteOffset) {
    let itemKeyProperty = new Civ5SaveStringProperty(byteOffset, null, saveData);
    byteOffset += itemKeyProperty.length;
    let itemValueProperty = new Civ5SaveBoolProperty(byteOffset, 4, saveData);
    byteOffset += itemValueProperty.length;

    this._items.set(itemKeyProperty.getValue(saveData), itemValueProperty);
    this.length = byteOffset - this.byteOffset;

    return byteOffset;
  }

  /**
   * @private
   */
  _getSize(saveData) {
    return this._size.getValue(saveData);
  }

  /**
   * @private
   */
  _setSize(saveData, newValue) {
    this._size.setValue(saveData, newValue);
  }

  /**
   * @ignore
   */
  getValue(saveData, itemKey) {
    if (this._items.has(itemKey)) {
      return this._items.get(itemKey).getValue(saveData);
    } else {
      return false;
    }
  }

  /**
   * @ignore
   */
  setValue(saveData, itemKey, newItemValue) {
    if (this._items.has(itemKey)) {
      this._items.get(itemKey).setValue(saveData, newItemValue);

    } else {
      return this._addItemToSaveData(saveData, itemKey, newItemValue);
    }
  }

  /**
   * @private
   */
  _addItemToSaveData(saveData, itemKey, newItemValue) {
    this._setSize(saveData, this._getSize(saveData) + 1);

    let itemKeyLengthArray = this._int32ToUint8Array(itemKey.length);
    let itemKeyArray = this._stringToUint8Array(itemKey);
    let itemValueArray = this._int32ToUint8Array(Number(newItemValue));
    let arrayToInsert = this._concatTypedArrays(
      this._concatTypedArrays(
        itemKeyLengthArray,
        itemKeyArray
      ),
      itemValueArray
    );

    let newSaveDataTypedArray = this._insertIntoTypedArray(
      new Uint8Array(saveData.buffer),
      arrayToInsert,
      this.byteOffset + this.length);
    let newSaveData = new Civ5SaveDataView(newSaveDataTypedArray.buffer);

    this._addItemToMap(newSaveData, this.byteOffset + this.length);

    return newSaveData;
  }

  /**
   * @private
   */
  // Inspired by https://stackoverflow.com/a/12965194/399105
  _int32ToUint8Array(int32) {
    let int32Array = new Uint8Array(4);
    for (let i = 0; i < int32Array.length; i++) {
      let byte = int32 & 0xff;
      int32Array[i] = byte;
      int32 = (int32 - byte) / 256;
    }
    return int32Array;
  }

  /**
   * @private
   */
  _stringToUint8Array(string) {
    let stringArray = new Uint8Array(string.length);
    for (let i = 0; i < string.length; i++) {
      stringArray[i] = string.charCodeAt(i);
    }
    return stringArray;
  }

  /**
   * @private
   */
  // https://stackoverflow.com/a/33703102/399105
  _concatTypedArrays(a, b) {
    var c = new (a.constructor)(a.length + b.length);
    c.set(a, 0);
    c.set(b, a.length);
    return c;
  }

  /**
   * @private
   */
  _insertIntoTypedArray(array, arrayToInsert, insertAtByteOffset) {
    return this._concatTypedArrays(
      this._concatTypedArrays(
        array.slice(0, insertAtByteOffset),
        arrayToInsert
      ),
      array.slice(insertAtByteOffset, array.length)
    );
  }
}
