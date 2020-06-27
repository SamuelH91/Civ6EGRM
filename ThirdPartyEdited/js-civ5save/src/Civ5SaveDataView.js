/**
 * @ignore
 */
// Subclassing DataView in babel requires https://www.npmjs.com/package/babel-plugin-transform-builtin-extend
export default class Civ5SaveDataView extends DataView {
  /**
   * @ignore
   */
  getString(byteOffset, byteLength) {
    if (typeof TextDecoder === 'function') {
      return new TextDecoder().decode(this.buffer.slice(byteOffset, byteOffset + byteLength));
    } else {
      // https://stackoverflow.com/a/17192845/399105
      let encodedString = String.fromCharCode.apply(null, new Uint8Array(this.buffer.slice(byteOffset,
        byteOffset + byteLength)));
      return decodeURIComponent(escape(encodedString));
    }
  }
}
