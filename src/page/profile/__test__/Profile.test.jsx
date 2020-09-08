import React from 'react';
import renderer from 'react-test-renderer';
import Profile from '../index.js';
// import {configure} from 'enzyme';
// import Adapter from 'enzyme-adapter-react-16';

// configure({ adapter: new Adapter() });

describe('Profile test', () => {
  test('should snapshot', () => {
    const comp = renderer.create(<Profile />);
    const tree = comp.toJSON();
    expect(tree).toMatchSnapshot();
  });
});