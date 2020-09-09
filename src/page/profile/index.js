import React from 'react';
// import PropTypes from 'prop-types'
import styles from './index.module.css';
// TODO: переход на профиль .../matcha/profile/name_user
// TODO: нужен ли класс

/**
 * Страниа профиля
*/
class Profile extends React.Component {
  state = {
    enabled: false,
  }
  /**
  * @return {obj} рендер странички с профилем
  */
  render() {
    return (<>
      <div className={styles.profile}>
        {/* TODO: запрос пользователя */}
        <div className={styles.fio}>
          <header className={styles.name}>{'Серый волк, 25'}</header>
          <p>{'м, гетеро'}</p>
          <p>{'ЮЗАО Москва'}</p>
        </div>
        <img className={styles.photo} src='volk.jpg' alt=""/>
      </div>
      <p className={styles.info}>{'Рейтинг славы: 10000000000000000'}</p>
      <p className={styles.info}>{'О себе: в поисках своего зайца'}</p>
      <button className={styles.button} onClick={() => {this.setState({enabled: !this.state.enabled})}}>
        {(!this.state.enabled && 'Показать') || 'Cпрятать'}</button>
    <> {this.state.enabled && <p className={styles.tags}>{'Мультипликация, животные, кулинария'}</p>} </>
    </>);
  }
}

export default Profile;
