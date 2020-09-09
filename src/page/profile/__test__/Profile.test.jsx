import React from 'react';
import renderer from 'react-test-renderer';
import Profile from '../index.js';
import { mount, configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('Profile test', () => {
  let wrap;
  let wrapper;

  test('should snapshot', () => {
    const comp = renderer.create(<Profile />);
    const tree = comp.toJSON();
    expect(tree).toMatchSnapshot();
  });

  beforeEach(() => {
    wrap = mount(<Profile />);
    wrapper = shallow(<Profile />);
  });

  it('should click button', () => {
    const comp = wrap.find(Profile).instance();
    if (comp.state.enabled = true) {
      expect(wrapper.find('button').simulate('onClick')
          .text()).toBe('Показать');
    }
    else {
      expect(wrapper.find('button').simulate('onClick')
          .text()).toBe('Спрятать');
      expect(wrapper.find('p').hasClass('tags').simulate('onClick')
          .text()).toBe('Мультипликация, животные, кулинария');
    }
  });
});
