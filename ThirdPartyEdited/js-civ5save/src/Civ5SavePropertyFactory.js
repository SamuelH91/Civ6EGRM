import Civ5SaveBoolProperty from './Civ5SaveBoolProperty';
import Civ5SaveDLCStringArray from './Civ5SaveDLCStringArray';
import Civ5SaveIntArray from './Civ5SaveIntArray';
import Civ5SaveIntProperty from './Civ5SaveIntProperty';
import Civ5SaveModsStringArray from './Civ5SaveModsStringArray';
import Civ5SaveProperty from './Civ5SaveProperty';
import Civ5SaveStringArray from './Civ5SaveStringArray';
import Civ5SaveStringProperty from './Civ5SaveStringProperty';
import Civ5SaveStringToBoolMap from './Civ5SaveStringToBoolMap';

/**
 * @ignore
 */
export default class Civ5SavePropertyFactory {
  /**
   * @ignore
   */
  static fromType(type, byteOffset, length, saveData) {
    switch (type) {
    case 'bool':
      return new Civ5SaveBoolProperty(byteOffset, length);

    case 'bytes':
      return new Civ5SaveProperty(byteOffset, length);

    case 'dlcStringArray':
      return new Civ5SaveDLCStringArray(byteOffset, saveData);

    case 'int':
      return new Civ5SaveIntProperty(byteOffset, length);

    case 'intArray':
      return new Civ5SaveIntArray(byteOffset, length, saveData);

    case 'modsStringArray':
      return new Civ5SaveModsStringArray(byteOffset, saveData);

    case 'string':
      return new Civ5SaveStringProperty(byteOffset, length, saveData);

    case 'stringArray':
      return new Civ5SaveStringArray(byteOffset, length, saveData);

    case 'stringToBoolMap':
      return new Civ5SaveStringToBoolMap(byteOffset, saveData);

    default:
      throw new Error(`Property type ${type} not handled`);
    }
  }
}
