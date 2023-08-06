(function () {
  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["styles"], {
    /***/
    "+EN/":
    /*!*************************!*\
      !*** ./src/styles.scss ***!
      \*************************/

    /*! no static exports found */

    /***/
    function EN(module, exports, __webpack_require__) {
      var api = __webpack_require__(
      /*! ../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */
      "LboF");

      var content = __webpack_require__(
      /*! !../node_modules/css-loader/dist/cjs.js??ref--13-1!../node_modules/postcss-loader/src??embedded!../node_modules/resolve-url-loader??ref--13-3!../node_modules/sass-loader/dist/cjs.js??ref--13-4!./styles.scss */
      "/I9Y");

      content = content.__esModule ? content["default"] : content;

      if (typeof content === 'string') {
        content = [[module.i, content, '']];
      }

      var options = {};
      options.insert = "head";
      options.singleton = false;
      var update = api(content, options);
      module.exports = content.locals || {};
      /***/
    },

    /***/
    "/I9Y":
    /*!*********************************************************************************************************************************************************************************************************************!*\
      !*** ./node_modules/css-loader/dist/cjs.js??ref--13-1!./node_modules/postcss-loader/src??embedded!./node_modules/resolve-url-loader??ref--13-3!./node_modules/sass-loader/dist/cjs.js??ref--13-4!./src/styles.scss ***!
      \*********************************************************************************************************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function I9Y(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony import */


      var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! ../node_modules/css-loader/dist/runtime/api.js */
      "JPst");
      /* harmony import */


      var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__); // Imports


      var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(true); // Module


      ___CSS_LOADER_EXPORT___.push([module.i, "/*\n======================================================\n=          Reset default Browser CSS Styles          =\n======================================================\n*/\n/* Remove default margin and padding for all */\n* {\n  margin: 0;\n  padding: 0;\n  box-sizing: border-box;\n}\n* :before,\n* :after {\n  box-sizing: inherit;\n}\n* :focus {\n  outline: none;\n}\n/* set body defaults */\nbody {\n  min-height: 100vh;\n  scroll-behavior: smooth;\n  text-rendering: optimizeSpeed;\n  display: block;\n  line-height: 1.5;\n  font-family: Arial, Helvetica, sans-serif;\n  /* reset html5 display-role for old browsers */\n  /* remove list styles on ul and ol */\n  /* set default image style */\n  /* inherit fonts */\n}\nbody footer,\nbody header,\nbody menu,\nbody nav,\nbody main,\nbody section,\nbody article,\nbody aside,\nbody details,\nbody figcaption,\nbody figure,\nbody hgroup {\n  display: block;\n}\nbody a {\n  text-decoration: none;\n}\nbody ul,\nbody ol {\n  list-style: none;\n  list-style-type: none;\n}\nbody img {\n  max-width: 100%;\n  display: block;\n}\nbody input,\nbody button,\nbody textarea,\nbody select {\n  font: inherit;\n}\n/*\n======================================================\n=       END OF Reset default Browser CSS Styles       =\n=======================================================\n*/\n/* set default value for colors*/\n/* set default value for fonts*/\n/* Mixin border-borded */\n/* divider */\nhr {\n  border: 1px solid whitesmoke;\n  clear: both;\n}\nh2 {\n  color: #0046AD;\n}\n/*common style from Grid View content */\n.row {\n  display: flex;\n  flex-wrap: wrap;\n  height: auto;\n  padding: 10px;\n  width: 100%;\n}\n/*left column */\n.side {\n  -ms-flex: 10%;\n  flex-direction: row;\n  flex: 10%;\n  background-color: #F9F8FF;\n  padding: 30px;\n  width: 20%;\n  min-width: 300px;\n}\n/* Main column */\n.main {\n  /* IE10 */\n  flex: 70%;\n  background-color: white;\n  padding: 30px;\n  height: 650px;\n  overflow: auto;\n}\n/* Table */\ntable {\n  font-family: arial, sans-serif;\n  border-collapse: collapse;\n  width: 100%;\n  font-size: 20px;\n}\ntable td,\ntable th {\n  border: 1px solid #FFFFFF;\n  text-align: center;\n  padding: 15px;\n}\ntable th {\n  width: 210px;\n}\ntable tr:nth-child(even) {\n  background-color: #F9F8FF;\n}\n/* select */\nlabel {\n  font-size: 1rem;\n  padding: 10px;\n}\nselect {\n  border: 1px solid #0046AD;\n  border-radius: 15px;\n  margin-top: 30px;\n  width: 100%;\n  font-size: 1.1rem;\n  padding: 5px;\n  color: white;\n  background-color: #0046AD;\n}\noption {\n  font-weight: bold;\n  padding: 13px;\n  border-bottom: 2px solid #FFFFFF;\n}\n@media screen and (max-width: 900px) {\n  .row {\n    flex-direction: column;\n    text-align: center;\n  }\n}\n.blueDivider {\n  margin-bottom: 0;\n  padding-bottom: 5px;\n  background-color: #0046AD;\n}", "", {
        "version": 3,
        "sources": ["webpack://src/styles.scss"],
        "names": [],
        "mappings": "AAAA;;;;CAAA;AAMA,8CAAA;AACA;EACI,SAAA;EACA,UAAA;EACA,sBAAA;AAAJ;AACK;;EAEG,mBAAA;AACR;AACK;EACG,aAAA;AACR;AAGA,sBAAA;AAMA;EAEI,iBAAA;EACA,uBAAA;EACA,6BAAA;EACA,cAAA;EACA,gBARS;EAST,yCAZS;EAaT,8CAAA;EAkBA,oCAAA;EAMA,4BAAA;EAKA,kBAAA;AAhCJ;AAII;;;;;;;;;;;;EAYI,cAAA;AAFR;AAII;EACI,qBAAA;AAFR;AAKI;;EAEI,gBAAA;EACA,qBAAA;AAHR;AAMI;EACI,eAAA;EACA,cAAA;AAJR;AAOI;;;;EAII,aAAA;AALR;AAQA;;;;CAAA;AAMA,gCAAA;AAoBA,+BAAA;AAUA,wBAAA;AAqBA,YAAA;AACA;EAVI,4BAAA;EAYA,WAAA;AAtDJ;AAyDA;EACI,cAzDW;AAGf;AAyDA,uCAAA;AAEA;EAEI,aAAA;EAEA,eAAA;EACA,YAAA;EACA,aAAA;EACA,WAAA;AAvDJ;AA2DA,eAAA;AAEA;EACI,aAAA;EACA,mBAAA;EACA,SAAA;EACA,yBAvEI;EAwEJ,aAAA;EACA,UAAA;EACA,gBAAA;AAzDJ;AA4DA,gBAAA;AACA;EAEI,SAAA;EACA,SAAA;EACA,uBAAA;EACA,aAAA;EACA,aAAA;EACA,cAAA;AAzDJ;AA4DA,UAAA;AACA;EACI,8BAAA;EACA,yBAAA;EACA,WAAA;EACA,eAAA;AAzDJ;AA0DI;;EA7DA,yBAAA;EAgEI,kBAAA;EACA,aAAA;AAxDR;AA0DI;EACI,YAAA;AAxDR;AA0DI;EACI,yBAxGA;AAgDR;AA4DA,WAAA;AACA;EACI,eAAA;EACA,aAAA;AAzDJ;AA4DA;EAjFI,yBAAA;EAmFA,mBAAA;EACA,gBAAA;EACA,WAAA;EACA,iBAAA;EACA,YAAA;EACA,YAAA;EACA,yBAlIW;AAyEf;AA4DA;EACI,iBAAA;EACA,aAAA;EACA,gCAAA;AAzDJ;AA4DA;EACI;IACI,sBAAA;IACA,kBAAA;EAzDN;AACF;AA4DA;EArGI,gBAAA;EACA,mBAAA;EACA,yBA/CW;AA2Ff",
        "sourcesContent": ["/*\n======================================================\n=          Reset default Browser CSS Styles          =\n======================================================\n*/\n\n/* Remove default margin and padding for all */\n* {\n    margin: 0;\n    padding: 0;\n    box-sizing: border-box;\n     :before,\n     :after {\n        box-sizing: inherit;\n    }\n     :focus {\n        outline: none;\n    }\n}\n\n/* set body defaults */\n$fontFamily: Arial,\nHelvetica,\nsans-serif;\n$lineHeight: 1.5;\n\nbody {\n    // min-width: 1208px;\n    min-height: 100vh;\n    scroll-behavior: smooth;\n    text-rendering: optimizeSpeed;\n    display: block;\n    line-height: $lineHeight;\n    font-family: $fontFamily;\n    /* reset html5 display-role for old browsers */\n    footer,\n    header,\n    menu,\n    nav,\n    main,\n    section,\n    article,\n    aside,\n    details,\n    figcaption,\n    figure,\n    hgroup {\n        display: block;\n    }\n    a {\n        text-decoration: none;\n    }\n    /* remove list styles on ul and ol */\n    ul,\n    ol {\n        list-style: none;\n        list-style-type: none;\n    }\n    /* set default image style */\n    img {\n        max-width: 100%;\n        display: block;\n    }\n    /* inherit fonts */\n    input,\n    button,\n    textarea,\n    select {\n        font: inherit;\n    }\n}\n/*\n======================================================\n=       END OF Reset default Browser CSS Styles       =\n=======================================================\n*/\n\n/* set default value for colors*/\n$micronasBlue: #0046AD;\n$skyBlue: #008ADC;\n$hoverBlue: #C1CFFF;\n$grey: #AAAABC;\n$darkGrey: #767687;\n$black:#454555;\n$white: #FFFFFF;\n$whiteSmoke: whitesmoke;\n$beige: #F9F8FF;\n$red: #DF4758;\n$warn: #FFBC58;\n$colorFooter: #F0F4F5;\n$borderColor: #74AEAC;\n$green: (\"darkGreen\": #008A65, \"hellGreen\": #6CFBCE, \"middleGreen\": #1FC198, \"btnGreen\": #01A860);\n$inactiveBackgroundColor: #aaa;\n$inactiveTextColor:black;\n$hoverBackgroundColor: #003399;\n$tabBorderColor: #ddd;\n\n/* set default value for fonts*/\n$menuItem: 20px; \n$card: 18px;\n$label: 14px;\n$button: 12px; \n$checkbox: 14px; \n$dropdown: 14px; \n$text: 12px;\n$footerHeight: 120px;\n\n/* Mixin border-borded */\n@mixin disabled {\n    color: $inactiveTextColor;\n    background: $inactiveBackgroundColor;\n    opacity: 0.3;\n}\n\n@mixin border($direction, $width, $style, $color) {\n    border-#{$direction}: $width $style $color;\n}\n\n@mixin solidBorder($width, $color) {\n    border: $width solid $color;\n}\n\n@mixin blueDivider {\n    margin-bottom: 0;\n    padding-bottom: 5px;\n    background-color: $micronasBlue;\n}\n\n/* divider */\nhr {\n    @include solidBorder(1px, $whiteSmoke);\n    clear: both;\n}\n\nh2 {\n    color: $micronasBlue;\n}\n\n/*common style from Grid View content */\n\n.row {\n    display: -ms-flexbox;\n    display: flex;\n    -ms-flex-wrap: wrap;\n    flex-wrap: wrap;\n    height: auto;\n    padding: 10px;\n    width: 100%;\n}\n\n\n/*left column */\n\n.side {\n    -ms-flex: 10%;\n    flex-direction: row;\n    flex: 10%;\n    background-color: $beige;\n    padding: 30px;\n    width: 20%;\n    min-width: 300px;\n}\n\n/* Main column */\n.main {\n    -ms-flex: 70%;\n    /* IE10 */\n    flex: 70%;\n    background-color: white;\n    padding:30px;\n    height: 650px;\n    overflow: auto;\n}\n\n/* Table */\ntable {\n    font-family: arial, sans-serif;\n    border-collapse: collapse;\n    width: 100%;\n    font-size: 20px;\n    td,\n    th {\n        @include solidBorder(1px, $white);\n        text-align: center;\n        padding: 15px;\n    }\n    th {\n        width: 210px;\n    }\n    tr:nth-child(even) {\n        background-color: $beige;\n    }\n}\n\n/* select */\nlabel {\n    font-size: 1rem;\n    padding: 10px;\n}\n\nselect {\n    @include solidBorder(1px, $micronasBlue);\n    border-radius: 15px;\n    margin-top: 30px;\n    width: 100%;\n    font-size: 1.1rem;\n    padding: 5px;\n    color: white;\n    background-color: $micronasBlue;\n}\n\noption {\n    font-weight: bold;\n    padding: 13px;\n    border-bottom: 2px solid $white;\n}\n\n@media screen and (max-width: 900px) {\n    .row {\n        flex-direction: column;\n        text-align: center;\n    }\n}\n\n.blueDivider {\n  @include blueDivider;\n}\n\n"],
        "sourceRoot": ""
      }]); // Exports

      /* harmony default export */


      __webpack_exports__["default"] = ___CSS_LOADER_EXPORT___;
      /***/
    },

    /***/
    3:
    /*!*******************************!*\
      !*** multi ./src/styles.scss ***!
      \*******************************/

    /*! no static exports found */

    /***/
    function _(module, exports, __webpack_require__) {
      module.exports = __webpack_require__(
      /*! /home/runner/work/Semi-ATE/Semi-ATE/ATE/Tester/TES/ui/angular/mini-sct-gui/src/styles.scss */
      "+EN/");
      /***/
    },

    /***/
    "JPst":
    /*!*****************************************************!*\
      !*** ./node_modules/css-loader/dist/runtime/api.js ***!
      \*****************************************************/

    /*! no static exports found */

    /***/
    function JPst(module, exports, __webpack_require__) {
      "use strict";
      /*
        MIT License http://www.opensource.org/licenses/mit-license.php
        Author Tobias Koppers @sokra
      */
      // css base code, injected by the css-loader
      // eslint-disable-next-line func-names

      module.exports = function (useSourceMap) {
        var list = []; // return the list of modules as css string

        list.toString = function toString() {
          return this.map(function (item) {
            var content = cssWithMappingToString(item, useSourceMap);

            if (item[2]) {
              return "@media ".concat(item[2], " {").concat(content, "}");
            }

            return content;
          }).join('');
        }; // import a list of modules into the list
        // eslint-disable-next-line func-names


        list.i = function (modules, mediaQuery, dedupe) {
          if (typeof modules === 'string') {
            // eslint-disable-next-line no-param-reassign
            modules = [[null, modules, '']];
          }

          var alreadyImportedModules = {};

          if (dedupe) {
            for (var i = 0; i < this.length; i++) {
              // eslint-disable-next-line prefer-destructuring
              var id = this[i][0];

              if (id != null) {
                alreadyImportedModules[id] = true;
              }
            }
          }

          for (var _i = 0; _i < modules.length; _i++) {
            var item = [].concat(modules[_i]);

            if (dedupe && alreadyImportedModules[item[0]]) {
              // eslint-disable-next-line no-continue
              continue;
            }

            if (mediaQuery) {
              if (!item[2]) {
                item[2] = mediaQuery;
              } else {
                item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
              }
            }

            list.push(item);
          }
        };

        return list;
      };

      function cssWithMappingToString(item, useSourceMap) {
        var content = item[1] || ''; // eslint-disable-next-line prefer-destructuring

        var cssMapping = item[3];

        if (!cssMapping) {
          return content;
        }

        if (useSourceMap && typeof btoa === 'function') {
          var sourceMapping = toComment(cssMapping);
          var sourceURLs = cssMapping.sources.map(function (source) {
            return "/*# sourceURL=".concat(cssMapping.sourceRoot || '').concat(source, " */");
          });
          return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
        }

        return [content].join('\n');
      } // Adapted from convert-source-map (MIT)


      function toComment(sourceMap) {
        // eslint-disable-next-line no-undef
        var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
        var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
        return "/*# ".concat(data, " */");
      }
      /***/

    },

    /***/
    "LboF":
    /*!****************************************************************************!*\
      !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
      \****************************************************************************/

    /*! no static exports found */

    /***/
    function LboF(module, exports, __webpack_require__) {
      "use strict";

      var isOldIE = function isOldIE() {
        var memo;
        return function memorize() {
          if (typeof memo === 'undefined') {
            // Test for IE <= 9 as proposed by Browserhacks
            // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
            // Tests for existence of standard globals is to allow style-loader
            // to operate correctly into non-standard environments
            // @see https://github.com/webpack-contrib/style-loader/issues/177
            memo = Boolean(window && document && document.all && !window.atob);
          }

          return memo;
        };
      }();

      var getTarget = function getTarget() {
        var memo = {};
        return function memorize(target) {
          if (typeof memo[target] === 'undefined') {
            var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

            if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
              try {
                // This will throw an exception if access to iframe is blocked
                // due to cross-origin restrictions
                styleTarget = styleTarget.contentDocument.head;
              } catch (e) {
                // istanbul ignore next
                styleTarget = null;
              }
            }

            memo[target] = styleTarget;
          }

          return memo[target];
        };
      }();

      var stylesInDom = [];

      function getIndexByIdentifier(identifier) {
        var result = -1;

        for (var i = 0; i < stylesInDom.length; i++) {
          if (stylesInDom[i].identifier === identifier) {
            result = i;
            break;
          }
        }

        return result;
      }

      function modulesToDom(list, options) {
        var idCountMap = {};
        var identifiers = [];

        for (var i = 0; i < list.length; i++) {
          var item = list[i];
          var id = options.base ? item[0] + options.base : item[0];
          var count = idCountMap[id] || 0;
          var identifier = "".concat(id, " ").concat(count);
          idCountMap[id] = count + 1;
          var index = getIndexByIdentifier(identifier);
          var obj = {
            css: item[1],
            media: item[2],
            sourceMap: item[3]
          };

          if (index !== -1) {
            stylesInDom[index].references++;
            stylesInDom[index].updater(obj);
          } else {
            stylesInDom.push({
              identifier: identifier,
              updater: addStyle(obj, options),
              references: 1
            });
          }

          identifiers.push(identifier);
        }

        return identifiers;
      }

      function insertStyleElement(options) {
        var style = document.createElement('style');
        var attributes = options.attributes || {};

        if (typeof attributes.nonce === 'undefined') {
          var nonce = true ? __webpack_require__.nc : undefined;

          if (nonce) {
            attributes.nonce = nonce;
          }
        }

        Object.keys(attributes).forEach(function (key) {
          style.setAttribute(key, attributes[key]);
        });

        if (typeof options.insert === 'function') {
          options.insert(style);
        } else {
          var target = getTarget(options.insert || 'head');

          if (!target) {
            throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
          }

          target.appendChild(style);
        }

        return style;
      }

      function removeStyleElement(style) {
        // istanbul ignore if
        if (style.parentNode === null) {
          return false;
        }

        style.parentNode.removeChild(style);
      }
      /* istanbul ignore next  */


      var replaceText = function replaceText() {
        var textStore = [];
        return function replace(index, replacement) {
          textStore[index] = replacement;
          return textStore.filter(Boolean).join('\n');
        };
      }();

      function applyToSingletonTag(style, index, remove, obj) {
        var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

        /* istanbul ignore if  */

        if (style.styleSheet) {
          style.styleSheet.cssText = replaceText(index, css);
        } else {
          var cssNode = document.createTextNode(css);
          var childNodes = style.childNodes;

          if (childNodes[index]) {
            style.removeChild(childNodes[index]);
          }

          if (childNodes.length) {
            style.insertBefore(cssNode, childNodes[index]);
          } else {
            style.appendChild(cssNode);
          }
        }
      }

      function applyToTag(style, options, obj) {
        var css = obj.css;
        var media = obj.media;
        var sourceMap = obj.sourceMap;

        if (media) {
          style.setAttribute('media', media);
        } else {
          style.removeAttribute('media');
        }

        if (sourceMap && btoa) {
          css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
        } // For old IE

        /* istanbul ignore if  */


        if (style.styleSheet) {
          style.styleSheet.cssText = css;
        } else {
          while (style.firstChild) {
            style.removeChild(style.firstChild);
          }

          style.appendChild(document.createTextNode(css));
        }
      }

      var singleton = null;
      var singletonCounter = 0;

      function addStyle(obj, options) {
        var style;
        var update;
        var remove;

        if (options.singleton) {
          var styleIndex = singletonCounter++;
          style = singleton || (singleton = insertStyleElement(options));
          update = applyToSingletonTag.bind(null, style, styleIndex, false);
          remove = applyToSingletonTag.bind(null, style, styleIndex, true);
        } else {
          style = insertStyleElement(options);
          update = applyToTag.bind(null, style, options);

          remove = function remove() {
            removeStyleElement(style);
          };
        }

        update(obj);
        return function updateStyle(newObj) {
          if (newObj) {
            if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
              return;
            }

            update(obj = newObj);
          } else {
            remove();
          }
        };
      }

      module.exports = function (list, options) {
        options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
        // tags it will allow on a page

        if (!options.singleton && typeof options.singleton !== 'boolean') {
          options.singleton = isOldIE();
        }

        list = list || [];
        var lastIdentifiers = modulesToDom(list, options);
        return function update(newList) {
          newList = newList || [];

          if (Object.prototype.toString.call(newList) !== '[object Array]') {
            return;
          }

          for (var i = 0; i < lastIdentifiers.length; i++) {
            var identifier = lastIdentifiers[i];
            var index = getIndexByIdentifier(identifier);
            stylesInDom[index].references--;
          }

          var newLastIdentifiers = modulesToDom(newList, options);

          for (var _i = 0; _i < lastIdentifiers.length; _i++) {
            var _identifier = lastIdentifiers[_i];

            var _index = getIndexByIdentifier(_identifier);

            if (stylesInDom[_index].references === 0) {
              stylesInDom[_index].updater();

              stylesInDom.splice(_index, 1);
            }
          }

          lastIdentifiers = newLastIdentifiers;
        };
      };
      /***/

    }
  }, [[3, "runtime"]]]);
})();
//# sourceMappingURL=styles-es5.js.map