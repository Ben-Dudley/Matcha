import React from 'react'
//import PropTypes from 'prop-types'
import styles from './index.module.css'
//TODO: переход на профиль .../matcha/profile/name_user
//TODO: нужен ли класс
class Profile extends React.Component {
    render() {
        return (<>
        <div className={styles.profile}>
        {/* TODO: запрос пользователя */}
        <div className={styles.name}>
        <header>{'Серый волк, 25'}</header>
        <p>{'м, гей'}</p>
        <p>{'ЮЗАО Москва'}</p>
        </div>
        <img className={styles.photo} src='volk.jpg' alt=""/>
        </div>
        <p className={styles.info}>{'Рейтинг славы: 10000000000000000'}</p>
        <p className={styles.info}>{'О себе: в поисках своего зайца'}</p>
        <p className={styles.tags}>{'Мультипликация, животные, кулинария'}</p>
        </>)    
    }
}

export default Profile