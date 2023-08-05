/*! For license information please see 33.5553a3a5.chunk.js.LICENSE.txt */
(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[33],{4028:function(e,t,r){"use strict";r.r(t),r.d(t,"default",(function(){return A}));var o=r(0),i=r.n(o),n=r(25),a=r(9),s=r(15),l=r(69),c=Object.freeze({default:"default",toggle:"toggle",toggle_round:"toggle_round"});Object.freeze({top:"top",right:"right",bottom:"bottom",left:"left"});function d(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,o)}return r}function u(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?d(Object(r),!0).forEach((function(t){h(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):d(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function h(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function b(e){var t=e.$disabled,r=e.$checked,o=e.$isIndeterminate,i=e.$isError,n=e.$error,a=e.$isHovered,s=e.$isActive,l=e.$theme,d=e.$checkmarkType===c.toggle,u=l.colors;return t?d?u.sliderTrackFillDisabled:r||o?u.tickFillDisabled:u.tickFill:(n||i)&&(o||r)?s?u.tickFillErrorSelectedHoverActive:a?u.tickFillErrorSelectedHover:u.tickFillErrorSelected:n||i?s?u.tickFillErrorHoverActive:a?u.tickFillErrorHover:u.tickFillError:o||r?s?u.tickFillSelectedHoverActive:a?u.tickFillSelectedHover:u.tickFillSelected:s?d?u.sliderTrackFillActive:u.tickFillActive:a?d?u.sliderTrackFillHover:u.tickFillHover:d?u.sliderTrackFill:u.tickFill}function g(e){var t=e.$disabled,r=e.$theme.colors;return t?r.contentSecondary:r.contentPrimary}var p=Object(s.a)("label",(function(e){var t=e.$disabled,r=e.$labelPlacement;return{flexDirection:"top"===r||"bottom"===r?"column":"row",display:"flex",alignItems:"top"===r||"bottom"===r?"center":"flex-start",cursor:t?"not-allowed":"pointer",userSelect:"none"}}));p.displayName="Root";var m=Object(s.a)("span",(function(e){var t=e.$checked,r=e.$disabled,o=e.$isError,i=e.$error,n=e.$isIndeterminate,a=e.$theme,s=e.$isFocusVisible,l=a.sizing,c=a.animation,d=r?a.colors.tickMarkFillDisabled:o||i?a.colors.tickMarkFillError:a.colors.tickMarkFill,u=encodeURIComponent('\n    <svg width="14" height="4" viewBox="0 0 14 4" fill="none" xmlns="http://www.w3.org/2000/svg">\n      <path d="M14 0.5H0V3.5H14V0.5Z" fill="'.concat(d,'"/>\n    </svg>\n  ')),h=encodeURIComponent('\n    <svg width="17" height="13" viewBox="0 0 17 13" fill="none" xmlns="http://www.w3.org/2000/svg">\n      <path d="M6.50002 12.6L0.400024 6.60002L2.60002 4.40002L6.50002 8.40002L13.9 0.900024L16.1 3.10002L6.50002 12.6Z" fill="'.concat(d,'"/>\n    </svg>\n  ')),g=a.borders.inputBorderRadius,p=function(e){var t=e.$disabled,r=e.$checked,o=e.$isError,i=e.$error,n=e.$isIndeterminate,a=e.$theme,s=e.$isFocusVisible,l=a.colors;return t?l.tickFillDisabled:r||n?"transparent":i||o?l.borderError:s?l.borderSelected:l.tickBorder}(e);return{flex:"0 0 auto",transitionDuration:c.timing200,transitionTimingFunction:c.easeOutCurve,transitionProperty:"background-image, border-color, background-color",width:l.scale700,height:l.scale700,left:"4px",top:"4px",boxSizing:"border-box",borderLeftStyle:"solid",borderRightStyle:"solid",borderTopStyle:"solid",borderBottomStyle:"solid",borderLeftWidth:"3px",borderRightWidth:"3px",borderTopWidth:"3px",borderBottomWidth:"3px",borderLeftColor:p,borderRightColor:p,borderTopColor:p,borderBottomColor:p,borderTopLeftRadius:g,borderTopRightRadius:g,borderBottomRightRadius:g,borderBottomLeftRadius:g,outline:s&&t?"3px solid ".concat(a.colors.accent):"none",display:"inline-block",verticalAlign:"middle",backgroundImage:n?"url('data:image/svg+xml,".concat(u,"');"):t?"url('data:image/svg+xml,".concat(h,"');"):null,backgroundColor:b(e),backgroundRepeat:"no-repeat",backgroundPosition:"center",backgroundSize:"contain",marginTop:a.sizing.scale0,marginBottom:a.sizing.scale0,marginLeft:a.sizing.scale0,marginRight:a.sizing.scale0}}));m.displayName="Checkmark";var f=Object(s.a)("div",(function(e){var t=e.$theme,r=e.$checkmarkType,o=t.typography;return u({flex:r===c.toggle?"auto":null,verticalAlign:"middle"},function(e){var t,r=e.$labelPlacement,o=void 0===r?"":r,i=e.$theme,n=i.sizing.scale300;switch(o){case"top":t="Bottom";break;case"bottom":t="Top";break;case"left":t="Right";break;default:case"right":t="Left"}return"rtl"===i.direction&&"Left"===t?t="Right":"rtl"===i.direction&&"Right"===t&&(t="Left"),h({},"padding".concat(t),n)}(e),{color:g(e)},o.LabelMedium,{lineHeight:"24px"})}));f.displayName="Label";var $=Object(s.a)("input",{opacity:0,width:0,height:0,overflow:"hidden",margin:0,padding:0,position:"absolute"});$.displayName="Input";var v=Object(s.a)("div",(function(e){if(e.$checkmarkType===c.toggle){var t=e.$theme.borders.useRoundedCorners?e.$theme.borders.radius200:null;return u({},Object(l.b)(e.$theme.borders.border300),{alignItems:"center",backgroundColor:e.$theme.colors.mono100,borderTopLeftRadius:t,borderTopRightRadius:t,borderBottomRightRadius:t,borderBottomLeftRadius:t,boxShadow:e.$isFocusVisible?"0 0 0 3px ".concat(e.$theme.colors.accent):e.$theme.lighting.shadow400,outline:"none",display:"flex",justifyContent:"center",height:e.$theme.sizing.scale800,width:e.$theme.sizing.scale800})}if(e.$checkmarkType===c.toggle_round){var r=e.$theme.colors.toggleFill;return e.$disabled?r=e.$theme.colors.toggleFillDisabled:e.$checked&&(e.$error||e.$isError)?r=e.$theme.colors.borderError:e.$checked&&(r=e.$theme.colors.toggleFillChecked),{backgroundColor:r,borderTopLeftRadius:"50%",borderTopRightRadius:"50%",borderBottomRightRadius:"50%",borderBottomLeftRadius:"50%",boxShadow:e.$isFocusVisible?"0 0 0 3px ".concat(e.$theme.colors.accent):e.$isHovered&&!e.$disabled?e.$theme.lighting.shadow500:e.$theme.lighting.shadow400,outline:"none",height:e.$theme.sizing.scale700,width:e.$theme.sizing.scale700,transform:e.$checked?"translateX(".concat("rtl"===e.$theme.direction?"-100%":"100%",")"):null,transition:"transform ".concat(e.$theme.animation.timing200)}}return{}}));v.displayName="Toggle";var k=Object(s.a)("div",(function(e){if(e.$checkmarkType===c.toggle){return{height:e.$theme.sizing.scale300,width:e.$theme.sizing.scale0,borderTopLeftRadius:e.$theme.borders.radius100,borderTopRightRadius:e.$theme.borders.radius100,borderBottomRightRadius:e.$theme.borders.radius100,borderBottomLeftRadius:e.$theme.borders.radius100,backgroundColor:e.$disabled?e.$theme.colors.sliderHandleInnerFillDisabled:e.$isActive&&e.$checked?e.$theme.colors.sliderHandleInnerFillSelectedActive:e.$isHovered&&e.$checked?e.$theme.colors.sliderHandleInnerFillSelectedHover:e.$theme.colors.sliderHandleInnerFill}}return e.$checkmarkType,c.toggle_round,{}}));k.displayName="ToggleInner";var y=Object(s.a)("div",(function(e){if(e.$checkmarkType===c.toggle){var t=e.$theme.borders.useRoundedCorners?e.$theme.borders.radius200:null;return{alignItems:"center",backgroundColor:b(e),borderTopLeftRadius:t,borderTopRightRadius:t,borderBottomRightRadius:t,borderBottomLeftRadius:t,display:"flex",height:e.$theme.sizing.scale600,justifyContent:e.$checked?"flex-end":"flex-start",marginTop:e.$theme.sizing.scale100,marginBottom:e.$theme.sizing.scale100,marginLeft:e.$theme.sizing.scale100,marginRight:e.$theme.sizing.scale100,width:e.$theme.sizing.scale1000}}if(e.$checkmarkType===c.toggle_round){var r=e.$theme.colors.toggleTrackFill;return e.$disabled?r=e.$theme.colors.toggleTrackFillDisabled:(e.$error||e.$isError)&&e.$checked&&(r=e.$theme.colors.tickFillError),{alignItems:"center",backgroundColor:r,borderTopLeftRadius:"7px",borderTopRightRadius:"7px",borderBottomRightRadius:"7px",borderBottomLeftRadius:"7px",display:"flex",height:e.$theme.sizing.scale550,marginTop:e.$theme.sizing.scale200,marginBottom:e.$theme.sizing.scale100,marginLeft:e.$theme.sizing.scale200,marginRight:e.$theme.sizing.scale100,width:e.$theme.sizing.scale1000}}return{}}));y.displayName="ToggleTrack";var R=r(32);function w(e){return(w="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"===typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function O(){return(O=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var o in r)Object.prototype.hasOwnProperty.call(r,o)&&(e[o]=r[o])}return e}).apply(this,arguments)}function T(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function j(e,t){for(var r=0;r<t.length;r++){var o=t[r];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function F(e,t){return!t||"object"!==w(t)&&"function"!==typeof t?L(e):t}function x(e){return(x=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function L(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function S(e,t){return(S=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function C(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}var B=function(e){return e.stopPropagation()},E=function(e){function t(){var e,r;T(this,t);for(var o=arguments.length,i=new Array(o),n=0;n<o;n++)i[n]=arguments[n];return C(L(r=F(this,(e=x(t)).call.apply(e,[this].concat(i)))),"state",{isFocused:r.props.autoFocus||!1,isFocusVisible:!1,isHovered:!1,isActive:!1}),C(L(r),"onMouseEnter",(function(e){r.setState({isHovered:!0}),r.props.onMouseEnter(e)})),C(L(r),"onMouseLeave",(function(e){r.setState({isHovered:!1,isActive:!1}),r.props.onMouseLeave(e)})),C(L(r),"onMouseDown",(function(e){r.setState({isActive:!0}),r.props.onMouseDown(e)})),C(L(r),"onMouseUp",(function(e){r.setState({isActive:!1}),r.props.onMouseUp(e)})),C(L(r),"onFocus",(function(e){r.setState({isFocused:!0}),r.props.onFocus(e),Object(R.d)(e)&&r.setState({isFocusVisible:!0})})),C(L(r),"onBlur",(function(e){r.setState({isFocused:!1}),r.props.onBlur(e),!1!==r.state.isFocusVisible&&r.setState({isFocusVisible:!1})})),C(L(r),"isToggle",(function(){return r.props.checkmarkType===c.toggle||r.props.checkmarkType===c.toggle_round})),r}var r,i,n;return function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&S(e,t)}(t,e),r=t,(i=[{key:"componentDidMount",value:function(){var e=this.props,t=e.autoFocus,r=e.inputRef;t&&r.current&&r.current.focus()}},{key:"render",value:function(){var e=this.props.checkmarkType,t=this.props,r=t.overrides,i=void 0===r?{}:r,n=t.onChange,s=t.labelPlacement,l=void 0===s?this.isToggle()?"left":"right":s,c=t.inputRef,d=t.isIndeterminate,u=t.isError,h=t.error,b=t.disabled,g=t.value,R=t.name,w=t.type,T=t.checked,j=t.children,F=t.required,x=t.title,L=t.ariaLabel,S=i.Root,C=i.Checkmark,E=i.Label,M=i.Input,z=i.Toggle,P=i.ToggleInner,H=i.ToggleTrack,I=Object(a.a)(S)||p,D=Object(a.a)(C)||m,V=Object(a.a)(E)||f,A=Object(a.a)(M)||$,_=Object(a.a)(z)||v,W=Object(a.a)(P)||k,U=Object(a.a)(H)||y,N={onChange:n,onFocus:this.onFocus,onBlur:this.onBlur},q={onMouseEnter:this.onMouseEnter,onMouseLeave:this.onMouseLeave,onMouseDown:this.onMouseDown,onMouseUp:this.onMouseUp},J={$isFocused:this.state.isFocused,$isFocusVisible:this.state.isFocusVisible,$isHovered:this.state.isHovered,$isActive:this.state.isActive,$isError:u,$error:h,$checked:T,$isIndeterminate:d,$required:F,$disabled:b,$value:g,$checkmarkType:e},Z=o.createElement(V,O({$labelPlacement:l},J,Object(a.b)(E)),j);return o.createElement(I,O({"data-baseweb":"checkbox",title:x||null,$labelPlacement:l},J,q,Object(a.b)(S)),("top"===l||"left"===l)&&Z,this.isToggle()?o.createElement(U,O({role:"checkbox","aria-checked":d?"mixed":T,"aria-invalid":h||u||null},J,Object(a.b)(H)),o.createElement(_,O({},J,Object(a.b)(z)),o.createElement(W,O({},J,Object(a.b)(P))))):o.createElement(D,O({role:"checkbox",checked:T,"aria-checked":d?"mixed":T,"aria-invalid":h||u||null},J,Object(a.b)(C))),o.createElement(A,O({value:g,name:R,checked:T,required:F,"aria-label":L,"aria-checked":d?"mixed":T,"aria-describedby":this.props["aria-describedby"],"aria-errormessage":this.props["aria-errormessage"],"aria-invalid":h||u||null,"aria-required":F||null,disabled:b,type:w,ref:c,onClick:B},J,N,Object(a.b)(M))),("bottom"===l||"right"===l)&&Z)}}])&&j(r.prototype,i),n&&j(r,n),t}(o.Component);C(E,"defaultProps",{overrides:{},checked:!1,disabled:!1,autoFocus:!1,isIndeterminate:!1,inputRef:o.createRef(),isError:!1,error:!1,type:"checkbox",checkmarkType:c.default,onChange:function(){},onMouseEnter:function(){},onMouseLeave:function(){},onMouseDown:function(){},onMouseUp:function(){},onFocus:function(){},onBlur:function(){}});var M=E,z=r(22),P=r(172),H=r(61),I=r(121),D=r(5);class V extends i.a.PureComponent{constructor(...e){super(...e),this.state={value:this.initialValue},this.setWidgetValue=e=>{const t=this.props.element.id;this.props.widgetMgr.setBoolValue(t,this.state.value,e)},this.onChange=e=>{const t=e.target.checked;this.setState({value:t},(()=>this.setWidgetValue({fromUi:!0})))},this.render=()=>{const e=this.props,t=e.theme,r=e.width,o=e.element,i=e.disabled,n=t.colors,a=t.fontSizes,s=t.radii,l={width:r};return Object(D.jsx)("div",{className:"row-widget stCheckbox",style:l,children:Object(D.jsxs)(M,{checked:this.state.value,disabled:i,onChange:this.onChange,overrides:{Root:{style:({$isFocused:e})=>({marginBottom:0,marginTop:0,paddingRight:a.twoThirdSmDefault,backgroundColor:e?n.darkenedBgMix15:"",borderTopLeftRadius:s.md,borderTopRightRadius:s.md,borderBottomLeftRadius:s.md,borderBottomRightRadius:s.md})},Checkmark:{style:({$isFocusVisible:e,$checked:t})=>{const r=t&&!i?n.primary:n.fadedText40;return{outline:0,boxShadow:e&&t?"0 0 0 0.2rem ".concat(Object(z.transparentize)(n.primary,.5)):"",borderLeftWidth:"2px",borderRightWidth:"2px",borderTopWidth:"2px",borderBottomWidth:"2px",borderLeftColor:r,borderRightColor:r,borderTopColor:r,borderBottomColor:r}}},Label:{style:{color:n.bodyText}}},children:[o.label,o.help&&Object(D.jsx)(I.d,{children:Object(D.jsx)(P.a,{content:o.help,placement:H.a.TOP_RIGHT})})]})})}}get initialValue(){const e=this.props.element.id,t=this.props.widgetMgr.getBoolValue(e);return void 0!==t?t:this.props.element.default}componentDidMount(){this.setWidgetValue({fromUi:!1})}}var A=Object(n.withTheme)(V)}}]);
//# sourceMappingURL=33.5553a3a5.chunk.js.map